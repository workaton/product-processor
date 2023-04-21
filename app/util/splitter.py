from __future__ import annotations

from abc import ABC, abstractmethod
import re
from typing import Sequence

from lxml import etree


class Splitter(ABC):
    """Base class for splitting data operations."""

    @abstractmethod
    async def split(self, data: bytes) -> Sequence[bytes]:
        """Split provided data into parts."""


class IwxxmSplitter(Splitter):
    """Splitter for IWXXM documents.

    This splitter separates each <meteorologicalInformation> element inside a
    <MeteorologicalBulletin> document into its own document, still wrapped
    inside the <MeteorologicalBulletin>.  The <bulletinIdentifier> element is
    also preserved for each output document.

    """

    async def split(self, data: bytes) -> Sequence[bytes]:
        root = etree.fromstring(data)
        identifier = next(iter(root.xpath('./collect:bulletinIdentifier', namespaces={
            'collect': 'http://def.wmo.int/collect/2014'
        })), None)
        products = root.xpath('./collect:meteorologicalInformation', namespaces={
            'collect': 'http://def.wmo.int/collect/2014'
        })

        return [self.__render_product(root, identifier, product) for product in products]

    def supports(self, data: bytes) -> bool:
        try:
            root = etree.fromstring(data)
            if len(root.xpath('/*[self::collect:MeteorologicalBulletin]', namespaces={
                'collect': 'http://def.wmo.int/collect/2014'
            })) < 1:
                return False
            if len(root.xpath('./*[self::collect:bulletinIdentifier]', namespaces={
                'collect': 'http://def.wmo.int/collect/2014'
            })) != 1:
                return False
            return True
        except Exception:
            return False

    def __render_product(self, root: etree.Element, identifier: etree.Element, product: etree.Element) -> bytes:
        new_root = etree.Element(root.tag, root.attrib)
        new_root.append(product)
        new_root.append(identifier)

        return etree.tostring(new_root)


class LineSplitter(Splitter):
    """Splitter for multiline documents."""

    async def split(self, data: bytes) -> Sequence[bytes]:
        return re.split(rb'\r{0,2}\n', data)
