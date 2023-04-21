from __future__ import annotations

from typing import Sequence
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.media_types import MediaTypes
from tac_to_xml import VolcanicAshAdvisoryEncoder

from .base import ConversionInput, ConversionResult, Converter


class VolcanicAshConverter(Converter):
    """Converts Volcanic Ash Advisory text products to IWXXM XML."""

    async def _convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        results = []
        data = inputs[0].data.decode('utf-8')
        encoder = VolcanicAshAdvisoryEncoder()
        for encoded in encoder.encode(data):
            result = ConversionResult(
                etree.tostring(encoded, encoding='UTF-8', xml_declaration=True),
                MediaTypes.APPLICATION_IWXXM_XML,
                id='VAA'
            )
            results.append(result)

        return results
