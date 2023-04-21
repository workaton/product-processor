from __future__ import annotations

from app.util.parser import GmlToGeojsonFilter
from lxml import etree
from ngitws.typing import JsonObject

from .base import IwxxmCollectiveExtractor, XmlExtractor


class TafExtractor(XmlExtractor):
    """Metadata extractor for TAF XML products."""

    XML_NAMESPACES = {
        'aixm': 'http://www.aixm.aero/schema/5.1.1',
        'gml': 'http://www.opengis.net/gml/3.2',
        'iwxxm11': 'http://icao.int/iwxxm/1.1',
        'iwxxm3': 'http://icao.int/iwxxm/3.0',
        'iwxxmus10': 'http://nws.weather.gov/schemas/IWXXM-US/1.0/Release',
        'saf': 'http://icao.int/saf/1.1'
    }

    def __init__(self):
        super().__init__(namespaces=self.XML_NAMESPACES)

    async def _extract(self, xml_tree: etree.ElementTree) -> JsonObject:
        parser = self.json_parser(xml_tree, filters=[GmlToGeojsonFilter()])
        if parser.contains('//iwxxm3:TAF'):
            root = '//iwxxm3:TAF'
        elif parser.contains('//iwxxm11:TAF'):
            root = '//iwxxm11:TAF'
        elif parser.contains('//iwxxmus10:TAF'):
            root = '//iwxxmus10:TAF'
        else:
            raise RuntimeError('XML document is not a recognized TAF product')

        if root == '//iwxxm3:TAF':
            issue_time = parser.first(f'{root}//iwxxm3:issueTime/gml:TimeInstant/gml:timePosition')
            location = parser.first(f'{root}//iwxxm3:aerodrome//aixm:locationIndicatorICAO')
            geometry = parser.first(f'{root}//iwxxm3:aerodrome//aixm:ARP/aixm:ElevatedPoint/gml:pos')
            start = parser.first(f'{root}//iwxxm3:validPeriod/gml:TimePeriod/gml:beginPosition')
            end = parser.first(f'{root}//iwxxm3:validPeriod/gml:TimePeriod/gml:endPosition')
        else:
            issue_time = parser.first(f'{root}//iwxxm11:issueTime/gml:TimeInstant/gml:timePosition')
            location = parser.first(f'{root}//saf:Aerodrome//saf:locationIndicatorICAO')
            geometry = parser.first(f'{root}//saf:Aerodrome//saf:ARP/gml:Point')
            start = parser.first(f'{root}//iwxxm11:validTime/gml:TimePeriod/gml:beginPosition')
            end = parser.first(f'{root}//iwxxm11:validTime/gml:TimePeriod/gml:endPosition')

        return {
            'issueTime': issue_time,
            'locationIdentifier': location,
            'geometry': geometry,
            'validPeriod': {
                'start': start,
                'end': end
            }
        }


class TafCollectiveExtractor(IwxxmCollectiveExtractor):
    """Metadata extractor for TAF XML collectives."""

    def __init__(self):
        super().__init__(TafExtractor())
