from __future__ import annotations

from abc import ABCMeta, abstractmethod
import json
import re
from typing import Collection, Mapping, Optional, Sequence

from lxml import etree
from multidict import MultiDict
from ngitws.typing import JsonObject, JsonType
from osgeo import ogr


class XmlParser:

    def __init__(self, xml_tree: etree.ElementTree, namespaces: Optional[Mapping[str, str]] = None):
        self.__namespaces = namespaces or {}
        self.__xml_tree = xml_tree

    def all(self, xpath: str) -> Sequence[etree.Element]:
        return self.__xml_tree.xpath(xpath, namespaces=self.__namespaces)

    def contains(self, xpath: str) -> bool:
        return bool(self.all(xpath))

    def first(self, xpath: str) -> Optional[etree.Element]:
        result = self.all(xpath)
        if result:
            return result[0]
        return None

    def last(self, xpath: str) -> Optional[etree.Element]:
        result = self.all(xpath)
        if result:
            return result[-1]
        return None


class JsonXmlParser:

    def __init__(
        self,
        xml_tree: etree.ElementTree,
        filters: Optional[Sequence[XmlToJsonFilter]] = None,
        namespaces: Optional[Mapping[str, str]] = None
    ):
        self.__filters = filters or []
        self.__parser = XmlParser(xml_tree, namespaces)

    def all(self, xpath: str, filters: Optional[Sequence[XmlToJsonFilter]] = None) -> Sequence[JsonType]:
        return [self._convert_element(element, filters=filters) for element in self.__parser.all(xpath)]

    def contains(self, xpath: str) -> bool:
        return self.__parser.contains(xpath)

    def first(self, xpath: str, filters: Optional[Sequence[XmlToJsonFilter]] = None) -> Optional[JsonType]:
        element = self.__parser.first(xpath)
        if element is None:
            return None

        return self._convert_element(element, filters=filters)

    def last(self, xpath: str, filters: Optional[Sequence[XmlToJsonFilter]] = None) -> Optional[JsonType]:
        element = self.__parser.last(xpath)
        if element is None:
            return None

        return self._convert_element(element, filters=filters)

    def _convert_element(self, element: etree.Element, filters: Optional[Sequence[XmlToJsonFilter]]) -> JsonType:
        return XmlToJsonFilterChain(filters or self.__filters)(element)


class XmlToJsonFilterChain:

    def __init__(self, filters: Sequence[XmlToJsonFilter]):
        self.__filters = [*filters, DefaultXmlToJsonFilter(filters)]

    def __call__(self, element: etree.Element) -> JsonType:
        return self.__filters.pop(0).filter(element, self)


class XmlToJsonFilter(metaclass=ABCMeta):

    @abstractmethod
    def filter(self, element: etree.Element, next: XmlToJsonFilterChain) -> JsonObject:
        pass


class DefaultXmlToJsonFilter(XmlToJsonFilter):

    def __init__(self, filters: Sequence[XmlToJsonFilter]):
        self.__filters = filters

    def filter(self, element: etree.Element, next: XmlToJsonFilterChain) -> JsonType:
        if isinstance(element, str):
            return element
        if len(element) == 0:
            return element.text

        children: MultiDict[JsonType] = MultiDict()
        for child in element:
            tag = re.sub(r'{.*}', '', child.tag)
            value = XmlToJsonFilterChain(self.__filters)(child)
            children.add(tag, value)

        json_out = {}
        for tag in children:
            values = children.getall(tag)
            if len(values) == 1:
                json_out[tag] = values[0]
            else:
                json_out[tag] = values

        return json_out


class GmlToGeojsonFilter(XmlToJsonFilter):

    DEFAULT_TAGS = [
        '{http://www.opengis.net/gml/3.2}LineString',
        '{http://www.opengis.net/gml/3.2}Point',
        '{http://www.opengis.net/gml/3.2}Polygon'
    ]

    def __init__(self, extra_tags: Optional[Collection[str]] = None, *, precision: int = 4):
        self.__precision = precision
        self.__tags = {*self.DEFAULT_TAGS, *(extra_tags or [])}

    def filter(self, element: etree.Element, next: XmlToJsonFilterChain) -> JsonObject:
        if isinstance(element, str):
            return next(element)

        if element.tag in self.__tags:
            return self._convert_geometry(element)
        elif element.tag == '{http://www.opengis.net/gml/3.2}pos':
            return self._convert_pos(element)
        elif element.tag == '{http://www.opengis.net/gml/3.2}coordinates':
            return self._convert_coordinates(element)

        return next(element)

    def _convert_geometry(self, element: etree.Element) -> JsonObject:
        gml = str(etree.tostring(element).decode('utf-8'))
        geometry = ogr.CreateGeometryFromGML(gml)
        geometry.FlattenTo2D()

        return json.loads(geometry.GetLinearGeometry().ExportToJson(options=[
            f'COORDINATE_PRECISION={self.__precision}'
        ]))

    def _convert_coordinates(self, element: etree.Element) -> JsonObject:
        assert element.tag == '{http://www.opengis.net/gml/3.2}coordinates'

        coords = element.text.strip()
        lat, lon, *unused = [round(float(coord.rstrip(',')), self.__precision) for coord in coords.split(' ')]

        return {
            'type': 'Point',
            'coordinates': [lat, lon]
        }

    def _convert_pos(self, element: etree.Element) -> JsonObject:
        assert element.tag == '{http://www.opengis.net/gml/3.2}pos'

        coords = element.text.strip()
        lat, lon, *unused = [round(float(coord), self.__precision) for coord in coords.split(' ')]

        return {
            'type': 'Point',
            'coordinates': [lat, lon]
        }
