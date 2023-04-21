from __future__ import annotations

import collections.abc
from typing import Any, Dict, Mapping, Optional, Sequence

from lxml import etree
from ngitws.collections import DotPathResolver
from ngitws.time import DateTimeConverter
from ngitws.typing import JsonObject
import pendulum
import xmltodict

from .base import XmlExtractor


class CapExtractor(XmlExtractor):
    """Metadata extractor for CAP XML products."""

    def __init__(self):
        super().__init__()

    async def _extract(self, xml_tree: etree.ElementTree) -> JsonObject:
        raw_document = xmltodict.parse(etree.tostring(xml_tree).decode('utf-8'), xml_attribs=False)
        document = DotPathResolver(raw_document)

        refs = self.__extract_references(document)
        if len(refs) > 0:
            document['alert.references'] = refs

        expires: Optional[pendulum.DateTime] = None
        # If there are multiple info nodes, ignore any non-US language ones and use the first US one.
        info_block = document.get('alert.info')
        if isinstance(info_block, collections.abc.Sequence):
            alert_infos: Sequence[Mapping] = document['alert.info']
            for info in alert_infos:
                language = info['language']
                if language is not None and language == 'en-US':
                    expires = DateTimeConverter().read_as_datetime(info['expires'])
                    document['alert.info'] = info
                    break
            if not expires:
                raise RuntimeError('No en-US language alert.info node found')
        elif isinstance(info_block, collections.abc.Mapping):
            info = info_block
            language = info['language']
            if not language or language == 'en-US':
                expires = DateTimeConverter().read_as_datetime(document['alert.info.expires'])
            else:
                raise RuntimeError('No en-US language alert.info node found')
        elif not info_block:
            raise RuntimeError('No alert.info block found')
        else:
            raise RuntimeError('Malformed alert.info block found')

        geometry = self.__extract_geometry(document)
        if geometry:
            document['alert.info.area.geometry'] = geometry
        if 'alert.info.area.polygon' in document:
            del document['alert.info.area.polygon']

        if expires is not None:
            document['localTimeZoneOffset'] = expires.format('Z')

        # Pull out the alert.info.parameter field where valueName is eventEndingTime and
        # place in the alert.info section, this makes query by ws team easier.
        alert_info_parameters: Sequence[Mapping] = document['alert.info.parameter']
        for param in alert_info_parameters:
            if param.get('valueName') == 'eventEndingTime':
                document['alert.info.eventEndingTime'] = param.get('value')

        return document.map

    def __extract_geometry(self, document: Mapping) -> Optional[Mapping]:
        """Convert the Doc.alert.info.area.polygon field to GeoJSON.

        Takes a string of the form:
            37.12,-108.78 37.23,-108.88 37.51,-108.45 37.42,-108.34 37.3,-108.28 37.12,-108.78

        """
        geometry: Dict[str, Any] = {}
        area = document.get('alert.info.area')

        assert isinstance(area, collections.abc.Mapping)
        if 'polygon' not in area:
            return None

        area_polygon = area.get('polygon')
        if isinstance(area_polygon, str):  # Polygon
            points = self.__build_polygon(area_polygon)

            geometry['type'] = 'Polygon'
            geometry['coordinates'] = points
        elif isinstance(area_polygon, collections.abc.Sequence):  # MultiPolygon
            polygons = []
            # Loop through list of polygons
            for poly in area_polygon:
                # Parse points and create an array of coordinates
                polygons.append(self.__build_polygon(poly))
            geometry['type'] = 'MultiPolygon'
            geometry['coordinates'] = polygons
        elif area_polygon is None:
            pass
        else:
            raise RuntimeError('Area polygon was not a string or sequence')

        return geometry

    def __extract_reference_ids(self, references: Sequence[Mapping[str, str]]) -> Sequence[str]:
        """Extract CAP reference IDs."""
        return [ref['identifier'] for ref in references]

    def __extract_references(self, document: Mapping) -> Sequence[Mapping[str, str]]:
        """Extract CAP references.

        Takes the form of 1 to n lines separated by space:
            w-nws.webmaster@noaa.gov,NWS-IDP-PROD-2128187-1986049,2016-11-10T11:00:24-05:00

        The resulting maps in the list have keys of "sender", "identifier", and
        "sent" for the respective comma-separated fields.

        """
        references = document.get('alert.references')
        if not references:
            return []

        split_refs = [ref.split(',') for ref in references.split(' ')]

        return [{
            'identifier': parts[1],
            'sender': parts[0],
            'sent': parts[2]
        } for parts in split_refs]

    def __build_polygon(self, polygon: str) -> Sequence[Sequence[Sequence[float]]]:
        # Reverse the coordinate list since latitude comes before longitude
        return [[[float(coord) for coord in list(reversed(vertex.split(',')))] for vertex in polygon.split(' ')]]
