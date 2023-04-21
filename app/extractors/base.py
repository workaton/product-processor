from __future__ import annotations

from abc import ABC, abstractmethod
import inspect
import logging
import pprint
from typing import Mapping, Optional, Sequence, TYPE_CHECKING

from app.util.parser import JsonXmlParser, XmlParser, XmlToJsonFilter
from app.util.splitter import IwxxmSplitter
from lxml import etree
from ngitws.logging import is_debug_enabled
from ngitws.typing import JsonObject


if TYPE_CHECKING:
    from app.resources import ResourceManager


class Extractor(ABC):
    """Base class for metadata extractors."""

    @classmethod
    async def create(cls, resources: ResourceManager) -> Extractor:
        return cls()

    @classmethod
    def description(cls) -> str:
        """Return a description of the extractor."""
        doc = inspect.getdoc(cls)
        if doc is None:
            raise RuntimeError(f'Missing docstring for {cls.__name__}')

        return doc.partition('\n')[0]

    @abstractmethod
    async def extract(self, data: bytes) -> JsonObject:
        """Extract metadata from byte string and returns it as a mapping."""


class XmlExtractor(Extractor):
    """Base class for extractors operating on XML documents."""

    def __init__(
        self,
        filters: Optional[Sequence[XmlToJsonFilter]] = None,
        namespaces: Optional[Mapping[str, str]] = None
    ):
        self._filters = filters or []
        self._namespaces = namespaces or {}

        self.__logger = logging.getLogger(__name__)

    async def extract(self, data: bytes) -> JsonObject:
        xml_tree = etree.fromstring(data)
        if is_debug_enabled():
            xml_tree_raw = etree.tostring(xml_tree, encoding='unicode', pretty_print=True)
            self.__logger.debug(f'Raw input XML:\n{xml_tree_raw}')

        result_json = await self._extract(xml_tree)
        if is_debug_enabled():
            self.__logger.debug(f'Extracted JSON:\n{pprint.pformat(result_json, indent=4)}')

        return result_json

    def json_parser(
        self,
        xml_tree: etree.ElementTree,
        filters: Optional[Sequence[XmlToJsonFilter]] = None
    ) -> JsonXmlParser:
        if filters is None:
            filters = self._filters
        return JsonXmlParser(xml_tree, filters=filters, namespaces=self._namespaces)

    def parser(self, xml_tree: etree.ElementTree) -> XmlParser:
        return XmlParser(xml_tree, namespaces=self._namespaces)

    @abstractmethod
    async def _extract(self, xml_tree: etree.ElementTree) -> JsonObject:
        pass


class IwxxmCollectiveExtractor(Extractor):
    """Base class for extractors operating on IWXXM XML collectives."""

    def __init__(self, extractor: XmlExtractor):
        super().__init__()
        self.__extractor = extractor

        self.__logger = logging.getLogger(__name__)

    async def extract(self, data: bytes) -> JsonObject:
        parts = await IwxxmSplitter().split(data)
        self.__logger.debug(f'Split collective product into {len(parts)} parts')

        return {
            'count': len(parts),
            'extracted': [await self.__extractor.extract(part) for part in parts]
        }
