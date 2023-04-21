from __future__ import annotations

import logging

from app.util.madis import MadisObservationGenerator
from ngitws.typing import JsonType

from .base import Extractor


class MadisCsvExtractor(Extractor):
    """Metadata extractor for MADIS CSV products."""

    def __init__(self):
        super().__init__()
        self.__generator = MadisObservationGenerator()

        self.__logger = logging.getLogger(__name__)

    async def extract(self, data: bytes) -> JsonType:
        madis_csv = data.decode('UTF-8')

        self.__logger.debug(f'Building observation from CSV data: {madis_csv}')

        return self.__generator.create_observation(madis_csv).as_dict()
