from __future__ import annotations

from app.util.parser import GmlToGeojsonFilter
from lxml import etree
from ngitws.typing import JsonObject

from .base import IwxxmCollectiveExtractor, XmlExtractor


class MetarExtractor(XmlExtractor):

    XML_NAMESPACES = {
        'aixm': 'http://www.aixm.aero/schema/5.1.1',
        'gml': 'http://www.opengis.net/gml/3.2',
        'iwxxm3': 'http://icao.int/iwxxm/3.0'
    }

    def __init__(self):
        super().__init__(namespaces=self.XML_NAMESPACES)

    async def _extract(self, xml_tree: etree.ElementTree) -> JsonObject:
        parser = self.json_parser(xml_tree, filters=[GmlToGeojsonFilter()])
        if parser.contains('//iwxxm3:METAR'):
            root = '//iwxxm3:METAR'
        elif parser.contains('//iwxxm3:SPECI'):
            root = '//iwxxm3:SPECI'
        else:
            raise RuntimeError('XML document is not a recognized METAR or SPECI product')

        issue_time = parser.first(f'{root}/iwxxm3:issueTime/gml:TimeInstant/gml:timePosition')
        location = parser.first(f'{root}//iwxxm3:aerodrome//aixm:designator')
        geometry = parser.first(f'{root}//iwxxm3:aerodrome//aixm:ARP/aixm:ElevatedPoint/gml:pos')

        return {
            'issueTime': issue_time,
            'locationIdentifier': location,
            'geometry': geometry
        }


class MetarCollectiveExtractor(IwxxmCollectiveExtractor):
    """Metadata extractor for METAR/SPECI XML collectives."""

    def __init__(self):
        super().__init__(MetarExtractor())
