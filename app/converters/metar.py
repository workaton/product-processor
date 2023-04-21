from __future__ import annotations

from typing import Sequence
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.media_types import MediaTypes
from tac_to_xml import MetarEncoder

from .base import ConversionInput, ConversionResult, ObsConverter


class MetarCollectiveConverter(ObsConverter):
    """Converts METAR collective text products to IWXXM XML."""

    async def _convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        data = inputs[0].data.decode('utf-8')
        encoder = MetarEncoder(self.obs_station_locator)
        encoded = encoder.encode(data)
        result = ConversionResult(
            etree.tostring(encoded.export(), encoding='UTF-8', xml_declaration=True),
            MediaTypes.APPLICATION_IWXXM_XML,
            id='METAR'
        )

        return [result]
