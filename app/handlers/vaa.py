from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ConversionHandler, ExtractionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class VolcanicAshConversionHandler(ConversionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('VAA'),
            file_catalog_id=resources.config.converters.vaa.file_catalog_id,
            prefetch=resources.config.converters.vaa.prefetch,
            publisher=await resources.nwstg_publisher(),
            subscription_id=resources.config.converters.vaa.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.vaa.is_enabled


class VolcanicAshExtractionHandler(ExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            extractor=await resources.extractor('VAA'),
            file_link_id='xml',
            prefetch=resources.config.extractors.vaa.prefetch,
            subscription_id=resources.config.extractors.vaa.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.vaa.is_enabled
