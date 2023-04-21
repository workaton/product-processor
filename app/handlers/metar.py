from __future__ import annotations

from typing import Sequence, TYPE_CHECKING

from app.media_types import MediaTypes
from app.util.splitter import IwxxmSplitter

from .base import CollectiveExtractionHandler, ConversionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class MetarCollectiveConversionHandler(ConversionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('METAR-COLLECTIVE'),
            file_catalog_id=resources.config.converters.metar.file_catalog_id,
            prefetch=resources.config.converters.metar.prefetch,
            publisher=await resources.nwstg_publisher(),
            subscription_id=resources.config.converters.metar.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.metar.is_enabled


class MetarCollectiveExtractionHandler(CollectiveExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            collective_file_link_id='xml',
            extractor=await resources.extractor('METAR'),
            part_file_catalog_id=resources.config.extractors.metar.file_catalog_id,
            part_file_link_id='xml',
            part_metadata_catalog_id=resources.config.extractors.metar.metadata_catalog_id,
            part_media_type=MediaTypes.APPLICATION_IWXXM_XML,
            prefetch=resources.config.extractors.metar.prefetch,
            subscription_id=resources.config.extractors.metar.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.metar.is_enabled

    async def _split_collective_data(self, data: bytes) -> Sequence[bytes]:
        return await IwxxmSplitter().split(data)
