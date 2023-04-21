from __future__ import annotations

import logging
import re
from typing import Sequence

from app.media_types import MediaTypes
from lxml import etree
from ncar_airsigmet_code.parse_airsigmet_intl import IntlSigmetParser
from ncar_airsigmet_code.parse_airsigmet_us import SigmetParser
from ncar_airsigmet_code.util import airsigmet_common
from ncar_airsigmet_code.writers.iwxxm_30_writer import IwxxmWriter
from ncar_airsigmet_code.writers.iwxxm_us_30_writer import IwxxmUsWriter

from .base import ConversionInput, ConversionResult, Converter


class SigmetConverter(Converter):
    """Converts AIRMET and SIGMET text products to IWXXM or IWXXM-US."""

    SIGMET_REGEX = rb'\d{3}[\n\r]+\w{4}\d{2} \w{4} \d{6}[\n\r]+(.*)[\n\r]+(.*)[\n\r]+(.*)[\n\r]+.*(SIGMET|AIRMET)'

    def __init__(self):
        self._domesticParser = None
        self._intlParser = None
        self._re = {}

        self.__logger = logging.getLogger(__name__)

        # Control characters \x01 === ^A and \x03 === ^C
        self._re['bulletin'] = re.compile(r'(\x01.*?\x03)', re.DOTALL)

        # if it doesn't look like 'WSUS...' then it should be parsed as an international even though it is US.
        # internal US SIGMETs look different than Intl US SIGMETs
        self._re['airsig_domestic'] = re.compile(r"""(
        ^(?P<prefix>.*?)\s*
        (?P<head>(?P<head_prefix>W(A|S|V)(?P<us_region>US|HW|AK)([0-9]+))\s(?P<issuing_center_id>[K|P][A-Z0-9]{3})\s(?P<head_time>([0-3][0-9])([0-2][0-9])([0-5][0-9])))\s
        (?P<remainder>.*?)
        )""", re.VERBOSE | re.DOTALL)

        self._re['sig_intl'] = re.compile(r"""(
        ^(?P<prefix>.*?)\s*
        (?P<head>W(?P<intl_type>C|S|V)([A-Z]{2})[0-9]{2}\s([A-Z][A-Z0-9]{3})\s([0-3][0-9])([0-2][0-9])([0-5][0-9])\s?(CC[A-Z])?)\s
        (?P<remainder>.*?)
        )""", re.VERBOSE | re.DOTALL)

        self._re['air_intl'] = re.compile(r"""(
        ^(?P<prefix>.*?)\s*
        (?P<head>W(A)([A-Z]{2})[0-9]{2}([A-Z]*)\s([A-Z][A-Z0-9]{3})\s([0-3][0-9])([0-2][0-9])([0-5][0-9])\s?(CC[A-Z])?)\s
        (?P<remainder>.*?)
        )""", re.VERBOSE | re.DOTALL)

        # Note: This regex is also used in parse_airsigmet_intl.py. Update there if you make changes here.
        self._re['intl_hdr'] = re.compile(r"""(
        ^(?P<prefix>.*?)\s*
        (?P<wmo>(?P<seq>[0-9]{3})?\s*
        (?P<ttaaii>[A-Z0-9]{6})\s
        (?P<cccc>[A-Z][A-Z0-9]{3})\s
        (?P<dd>[0-3][0-9])(?P<hh>[0-2][0-9])(?P<mm>[0-5][0-9])\s*
        (?P<bbb>[CAR]{2}[A-Z])?\s*
        (?P<awips>[A-Z]{3}[A-Z0-9]{3})?
        )
        )""", re.VERBOSE | re.DOTALL)

        self.Errors = 0
        self.Warnings = 0
        self.Bulletins = 0

    async def _convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        results = []
        data = inputs[0].data.decode('utf-8')
        parsed_sigmets = self.parse_file(data)
        # parsed_sigmets = self.parse_file(data, verbosity=3)
        for sig in parsed_sigmets:
            sig_xml = self.produce_xml(sigmet=sig)
            # TODO: could be IWXXM or IWXXM-US
            result = ConversionResult(str.encode(sig_xml), MediaTypes.APPLICATION_IWXXM_XML, id='SIGMET')
            results.append(result)

        return results

    # This was slightly modified from NCAR's split_airsigmet.py tool.
    def parse_file(self, product, verbosity=0):
        """Parse raw product and split bulletins into AIRMETs or SIGMETs and output XML.

        :param product:                     input stream containing the data
        :param verbosity:                   desired verbosity level, for diagnostic logging
        :return:
            a collection of resulting air/sigmet parsed parameter objects
        """
        bulletins = self._re['bulletin'].findall(product)

        # if no bulletins are found we may be passed the raw text without WMO headers
        self.__logger.debug(f'Found {len(bulletins)} bulletin items')
        if len(bulletins) == 0:
            if verbosity >= 3:
                self.__logger.debug('Parsing bulletin items as raw text')
            bulletins = [product]

        sigmets = []
        for text in bulletins:
            text = airsigmet_common.strip_non_ascii(text)

            if text.find(' TEST ') >= 0 or text.find(' EXERCISE ') >= 0:
                self.__logger.info(f'Ignoring test bulletin: "{" ".join(text.split())}"')
                continue

            verbosity = verbosity

            if verbosity >= 3:
                self.__logger.debug('Start bulletin')

            dom = self._re['airsig_domestic'].match(text)
            intl_sig = self._re['sig_intl'].match(text)
            intl_air = self._re['air_intl'].match(text)

            is_domestic = True
            if dom and intl_sig:
                # Call this domestic unless it's an Alaska SIGMET. airTrafficUnit will not be KKCI
                m = self._re['intl_hdr'].match(text)
                if m:
                    d = m.groupdict()
                    air_traffic_unit = d['cccc']
                    if air_traffic_unit is not None and 'KKCI' not in air_traffic_unit:
                        is_domestic = False

            # if dom and not intl_sig: # Alaska SIGMETs must be parsed as international reports
            if dom and is_domestic:
                has_sub_bulletins = False
                if not self._domesticParser:
                    self._domesticParser = SigmetParser(verbosity)

                d = dom.groupdict()
                if verbosity >= 2:
                    if d['head'][1:2] == 'A':
                        self.__logger.debug('Domestic AIRMET: ' + d['head'])

                        # Handle Alaska and Hawaii AIRMETs, with different hazards lumped into one bulletin...
                        if d['us_region'] is not None and (d['us_region'] == 'AK' or d['us_region'] == 'HW'):
                            self.__logger.debug(
                                f'Checking {d["us_region"]} AIRMET bulletin to see if it contains multiple bulletins'
                            )
                            temp_parser = SigmetParser(verbosity)
                            sub_bulletins = temp_parser.split_AKHI_AIRMETs(text, d['us_region'])
                            if len(sub_bulletins) > 1:
                                self.__logger.debug(f'Splitting AIRMET into {str(len(sub_bulletins))} sub-bulletins...')
                                has_sub_bulletins = True

                                for bul in sub_bulletins:
                                    sigmets.extend(self._domesticParser.parse(bul))

                    else:
                        self.__logger.debug('Domestic SIGMET: ' + d['head'])

                if not has_sub_bulletins:
                    sigmets.extend(self._domesticParser.parse(text))

            elif intl_sig:
                d = intl_sig.groupdict()
                if verbosity >= 2:
                    self.__logger.debug('International SIGMET: ' + d['head'])

                if not self._intlParser:
                    self._intlParser = IntlSigmetParser(verbosity)

                typ = d['intl_type']
                if typ == 'V':
                    sigmets.extend(self._intlParser.parse(text))
                elif typ == 'C':
                    sigmets.extend(self._intlParser.parse(text))
                elif typ == 'S':
                    sigmets.extend(self._intlParser.parse(text))
                else:
                    self.__logger.warning("Unknown international SIGMET type: %s. Halting.  Raw file: %s" % (type))

            elif intl_air:

                d = intl_air.groupdict()
                if verbosity >= 2:
                    self.__logger.debug('International AIRMET: ' + d['head'])

                if not self._intlParser:
                    self._intlParser = IntlSigmetParser(verbosity)

                sigmets.extend(self._intlParser.parse(text))

            else:
                self.__logger.warning("Could not determine report/bulletin type in '%s'. Processing as raw text")
                if not self._intlParser:
                    self._intlParser = IntlSigmetParser(verbosity)

                sigmets.extend(self._intlParser.parse(text))

        if verbosity >= 3:
            self.__logger.debug('End bulletin')
        if verbosity >= 1:
            self.__logger.info("Finished parsing %s bulletins" % len(bulletins))

        errors = 0
        warnings = 0
        if self._intlParser:
            if verbosity >= 3:
                self.__logger.info('International parser: %s warnings, %s errors' % (
                    self._intlParser.getNWarnings(),
                    self._intlParser.getNErrors()
                ))
            errors = self._intlParser.getNErrors()
            warnings = self._intlParser.getNWarnings()
            self._intlParser.clearErrorsWarnings()
        if self._domesticParser:
            if verbosity >= 3:
                self.__logger.info('Domestic parser: %s warnings, %s errors' % (
                    self._domesticParser.getNWarnings(),
                    self._domesticParser.getNErrors()
                ))
            errors += self._domesticParser.getNErrors()
            warnings += self._domesticParser.getNWarnings()
            self._domesticParser.clearErrorsWarnings()

        return sigmets

    # Produce the iwxxm output for the sigmet.  The sigmet argument is a Sigmet object, not a string
    def produce_xml(self, sigmet):
        if (self._domesticParser):
            iwxxm_writer = IwxxmUsWriter()
        else:
            iwxxm_writer = IwxxmWriter()
        root_elem, text_id, uuid = iwxxm_writer.create_xml(airsigmetdata=sigmet)
        xmlstr = etree.tostring(root_elem, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        xmlstr = xmlstr.decode('utf-8')
        # replace single quotes with double, as is convention
        return xmlstr.replace("<?xml version='1.0' encoding='UTF-8'?>", "<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
