import logging
import re

from typing import Optional, TYPE_CHECKING, Dict, Any

class FwsApp(object):
    '''FWS daemon application'''

    def __init__(self, parser:Any, provider:str):
        self.parser:FwsParser = parser
        self.provider:str = provider
        self.product:FwsProduct = None
        self.__logger = logging.getLogger(__name__)

    def run(self) -> None:
        result: Dict[str, Any] = self.main(self.provider)
        self.product = FwsProduct(result)

        self.__logger.info('Exiting FwsApp program')

    def main(self, message:str) -> Dict[str, Any]:
        '''Reads FWS product and store forecast data in SPOT database'''

        try:
            result = self.parser.parse(message)
            return result
        except LegacyTag as e:
            self.__logger.info('Discarding legacy product -- {0}'.format(e))
        except InvalidTag as e:
            self.__logger.warning('Discarding unrecognized tag -- {0}'.format(e))
        except InvalidProduct as e:
            self.__logger.warning('Discarding invalid product\n{0}'.format(e))
        # return result

    def get_product(self):
        return self.product


class FwsParser(object):

    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def parse(self, product:str)-> Dict[str, Any]:
        '''Parse an FWS product for information to store in database.'''

        REGEX_FORECAST_TEXT = r'^(SPOT|FIRE WEATHER PLANNING) FORECAST FOR'
        REGEX_FORECASTER = r'^FORECASTER\.\.\.(.*)$'
        REGEX_TAG_LINE = r'^\.TAG\s+(.*)$'
        REGEX_VALID_TAG = r'^([0-9]{7})\.([0-9]+)\/[A-Z]+$'
        REGEX_LEGACY_TAG = r'^[0-9]{8}\.[A-Z0-9_]+\.[0-9]{2}\/[A-Z]+$'
        REGEX_CORRECTED = r'\.\.\.\s*CORRECTED\s*(?:...)?$'

        tag_match = re.search(REGEX_TAG_LINE, product, re.M | re.I)
        if not tag_match:
            raise InvalidProduct(product)
        
        tag = tag_match.group(1).strip()
        if re.match(REGEX_LEGACY_TAG, tag):
            raise LegacyTag(tag)

        valid_tag = re.match(REGEX_VALID_TAG, tag)
        if not valid_tag:
            raise InvalidTag(tag)

        pos = re.search(REGEX_FORECAST_TEXT, product, re.M | re.I)
        if not pos:
            raise InvalidProduct(product)

        id = valid_tag.group(1)
        update = valid_tag.group(2)
        text = product[pos.start():]

        corrected = bool(re.search(REGEX_CORRECTED, text, re.M | re.I))

        forecaster_match = re.search(REGEX_FORECASTER, text, re.M | re.I)
        forecaster = forecaster_match.group(1) if forecaster_match else ''

        return {
            'id': id,
            'update': update,
            'text': text,
            'forecaster': forecaster,
            'corrected': corrected
        }


class FwsProduct(object):

    def __init__(self, result):
        self.id = result["id"]
        self.update = result["update"]
        self.text = result["text"]
        self.forecaster = result["forecaster"]
        self.corrected = result["corrected"]

        self.__logger = logging.getLogger(__name__)



class InvalidProduct(Exception):
    '''FWS product is invalid or malformed.'''


class InvalidTag(Exception):
    '''FWS product has an unrecognized tag.'''


class LegacyTag(Exception):
    '''FWS product was issued using old SPOT system.'''
