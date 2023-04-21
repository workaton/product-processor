from __future__ import annotations

import logging
from typing import Sequence
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.media_types import MediaTypes
from tac_to_xml import TafEncoder

from .base import ConversionInput, ConversionResult, ObsConverter


class TafCollectiveConverter(ObsConverter):
    """Converts TAF collective text products to IWXXM XML."""

    PLAIN_TEXT_TYPE = 'text/plain;charset=UTF-8'

    async def _convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        self.__logger = logging.getLogger(__name__)
        media_type = str(inputs[0].media_type)
        is_text = media_type == str(MediaTypes.TEXT_PLAIN)
        is_text_utf = media_type == TafCollectiveConverter.PLAIN_TEXT_TYPE
        if (not (is_text or is_text_utf)):
            self.__logger.info('Input is not text.  No conversion required')
            return [ConversionResult(inputs[0].data, inputs[0].media_type, id='TAF')]
        data = inputs[0].data.decode('utf-8')
        encoder = TafEncoder(self.obs_station_locator)
        encoded = encoder.encode(data)
        result = ConversionResult(
            etree.tostring(encoded.export(), encoding='UTF-8', xml_declaration=True),
            MediaTypes.APPLICATION_IWXXM_XML,
            id='TAF')

        return [result]
