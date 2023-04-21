from __future__ import annotations

from app.util.parser import GmlToGeojsonFilter
from lxml import etree
from ngitws.typing import JsonObject

from .base import XmlExtractor


class CwaExtractor(XmlExtractor):
    """Metadata extractor for CWA XML products."""

    XML_NAMESPACES = {
        'aixm': 'http://www.aixm.aero/schema/5.1.1',
        'gml': 'http://www.opengis.net/gml/3.2',
        'iwxxm11': 'http://icao.int/iwxxm/1.1',
        'iwxxm3': 'http://icao.int/iwxxm/3.0',
        'iwxxmus10': 'http://nws.weather.gov/schemas/IWXXM-US/1.0/Release',
        'om': 'http://www.opengis.net/om/2.0',
        'saf': 'http://icao.int/saf/1.1',
        'uswx10': 'http://nws.weather.gov/schemas/USWX/1.0',
        'xlink': 'http://www.w3.org/1999/xlink'
    }

    def __init__(self):
        super().__init__(namespaces=self.XML_NAMESPACES)

    async def _extract(self, xml_tree: etree.ElementTree) -> JsonObject:
        parser = self.json_parser(xml_tree, filters=[GmlToGeojsonFilter()])
        if not parser.contains('//uswx10:CenterWeatherAdvisory'):
            raise RuntimeError('XML document is not a recognized CWA product')

        cwsu_id = parser.first('//uswx10:centerWeatherServiceUnit/saf:designator')
        sequence_issuance = parser.first('//uswx10:sequenceIssuance')
        phenomenon_start = parser.first(
            '//uswx10:centerWeatherAdvisoryRecord/om:phenomenonTime/gml:TimePeriod/gml:beginPosition'
        )
        phenomenon_end = parser.first(
            '//uswx10:centerWeatherAdvisoryRecord/om:phenomenonTime/gml:TimePeriod/gml:endPosition')
        result_time = parser.first(
            '//uswx10:centerWeatherAdvisoryRecord/om:resultTime/gml:TimeInstant/gml:timePosition'
        )
        observed_property = parser.first('//uswx10:centerWeatherAdvisoryRecord/om:observedProperty/@xlink:href')
        geometry = parser.first('//uswx10:centerWeatherAdvisoryRecord/om:featureOfInterest//gml:location/*[1]')
        statement_text = parser.first(
            '//uswx10:centerWeatherAdvisoryRecord/om:result/uswx10:CenterWeatherAdvisoryStatement'
            '/uswx10:centerWeatherAdvisoryText'
        )

        return {
            'cwsuIdentifier': cwsu_id,
            'sequenceIssuance': sequence_issuance,
            'phenomenonTime': {
                'start': phenomenon_start,
                'end': phenomenon_end
            },
            'resultTime': result_time,
            'observedProperty': observed_property,
            'geometry': geometry,
            'statementText': statement_text
        }
