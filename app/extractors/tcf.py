from __future__ import annotations

from lxml import etree
from ngitws.typing import JsonObject

from .base import XmlExtractor


class TcfExtractor(XmlExtractor):
    """Metadata extractor for TCF XML products."""

    async def _extract(self, xml_tree: etree.ElementTree) -> JsonObject:
        return {}
