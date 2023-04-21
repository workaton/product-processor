from __future__ import annotations

from typing import Sequence, TYPE_CHECKING

from app.media_types import MediaTypes
from app.util.splitter import IwxxmSplitter

from .base import CollectiveExtractionHandler, ConversionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class TafCollectiveConversionHandler(ConversionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('TAF-COLLECTIVE'),
            file_catalog_id=resources.config.converters.taf.file_catalog_id,
            prefetch=resources.config.converters.taf.prefetch,
            publisher=await resources.nwstg_publisher(),
            subscription_id=resources.config.converters.taf.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.taf.is_enabled


class TafCollectiveExtractionHandler(CollectiveExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            collective_file_link_id='xml',
            extractor=await resources.extractor('TAF'),
            part_file_catalog_id=resources.config.extractors.taf.file_catalog_id,
            part_file_link_id='xml',
            part_metadata_catalog_id=resources.config.extractors.taf.metadata_catalog_id,
            part_media_type=MediaTypes.APPLICATION_IWXXM_XML,
            prefetch=resources.config.extractors.taf.prefetch,
            subscription_id=resources.config.extractors.taf.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.taf.is_enabled

    async def _split_collective_data(self, data: bytes) -> Sequence[bytes]:
        return await IwxxmSplitter().split(data)
