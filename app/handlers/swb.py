from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ConversionHandler, ExtractionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class SwbConversionHandler(ConversionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('SWB'),
            file_catalog_id=resources.config.converters.swb.file_catalog_id,
            prefetch=resources.config.converters.swb.prefetch,
            subscription_id=resources.config.converters.swb.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.swb.is_enabled


class SwbExtractionHandler(ExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            extractor=await resources.extractor('SWB'),
            file_link_id='xml',
            prefetch=resources.config.extractors.swb.prefetch,
            subscription_id=resources.config.extractors.swb.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.swb.is_enabled
