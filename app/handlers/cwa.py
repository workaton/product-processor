from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ConversionHandler, ExtractionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class CwaConversionHandler(ConversionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('CWA'),
            file_catalog_id=resources.config.converters.cwa.file_catalog_id,
            prefetch=resources.config.converters.cwa.prefetch,
            subscription_id=resources.config.converters.cwa.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.cwa.is_enabled


class CwaExtractionHandler(ExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            extractor=await resources.extractor('CWA'),
            file_link_id='xml',
            prefetch=resources.config.extractors.cwa.prefetch,
            subscription_id=resources.config.extractors.cwa.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.cwa.is_enabled
