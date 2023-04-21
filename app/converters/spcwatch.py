from __future__ import annotations

from typing import Sequence
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.media_types import MediaTypes
from tac_to_xml import SPCWatchEncoder

from .base import ConversionInput, ConversionResult, Converter


class SpcWatchConverter(Converter):
    """Converts SAW and SEL text products to USWX XML.

    This converter requires a different interface as the conversion process is
    dependent on both TAC products at once.

    """

    async def _convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        saw_data = None
        sel_data = None

        for input in inputs:
            if input.id == 'SAW':
                saw_data = input.data.decode('utf-8')
            elif input.id == 'SEL':
                sel_data = input.data.decode('utf-8')
            else:
                return []

        if saw_data and sel_data:
            encoder = SPCWatchEncoder()
            encoded_saw, encoded_sel = encoder.encode(saw_data, sel_data)
            saw_result = ConversionResult(
                etree.tostring(encoded_saw, encoding='UTF-8', xml_declaration=True),
                MediaTypes.APPLICATION_USWX_XML,
                id='SAW'
            )
            sel_result = ConversionResult(
                etree.tostring(encoded_sel, encoding='UTF-8', xml_declaration=True),
                MediaTypes.APPLICATION_USWX_XML,
                id='SEL'
            )

            return [saw_result, sel_result]
        else:
            return []
