from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ConversionHandler, ExtractionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class PirepConversionHandler(ConversionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('PIREP'),
            file_catalog_id=resources.config.converters.pirep.file_catalog_id,
            prefetch=resources.config.converters.pirep.prefetch,
            subscription_id=resources.config.converters.pirep.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.pirep.is_enabled


class PirepExtractionHandler(ExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            extractor=await resources.extractor('PIREP'),
            file_link_id='xml',
            prefetch=resources.config.extractors.pirep.prefetch,
            subscription_id=resources.config.extractors.pirep.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.pirep.is_enabled
