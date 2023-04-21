from __future__ import annotations

from typing import Sequence
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.media_types import MediaTypes
from tac_to_xml import CWAEncoder

from .base import ConversionInput, ConversionResult, Converter


class CwaConverter(Converter):
    """Converts CWA text products to USWX XML."""

    async def _convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        data = inputs[0].data.decode('utf-8')
        encoder = CWAEncoder()
        encoded = encoder.encode(data)
        result = ConversionResult(
            etree.tostring(encoded, encoding='UTF-8', xml_declaration=True),
            MediaTypes.APPLICATION_USWX_XML,
            id='CWA'
        )

        return [result]
