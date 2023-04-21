from __future__ import annotations

import json
from typing import Sequence
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.media_types import MediaTypes
from tac_to_xml import MADISEncoder

from .base import ConversionInput, ConversionResult, Converter


class MadisJsonConverter(Converter):
    """Converts MADIS catalog record metadata to USWX XML."""

    async def _convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        encoder = MADISEncoder()
        metadata = json.loads(inputs[0].data)
        encoded = encoder.encode(metadata)
        result = ConversionResult(
            etree.tostring(encoded, encoding='UTF-8', xml_declaration=True),
            MediaTypes.APPLICATION_USWX_XML,
            id='MADIS'
        )

        return [result]
