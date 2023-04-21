from __future__ import annotations

from lxml import etree
from ngitws.typing import JsonObject

from .base import XmlExtractor


class CsfpfExtractor(XmlExtractor):
    """Metadata extractor for CSFPF XML products."""

    async def _extract(self, xml_tree: etree.ElementTree) -> JsonObject:
        return {}
