from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ConversionHandler, ExtractionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class WtaConversionHandler(ConversionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('WTA'),
            file_catalog_id=resources.config.converters.wta.file_catalog_id,
            prefetch=resources.config.converters.wta.prefetch,
            subscription_id=resources.config.converters.wta.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.wta.is_enabled


class WtaExtractionHandler(ExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            extractor=await resources.extractor('WTA'),
            file_link_id='xml',
            prefetch=resources.config.extractors.wta.prefetch,
            subscription_id=resources.config.extractors.wta.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.wta.is_enabled
