from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ConversionHandler, ExtractionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class SigmetConversionHandler(ConversionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('SIGMET'),
            file_catalog_id=resources.config.converters.sigmet.file_catalog_id,
            prefetch=resources.config.converters.sigmet.prefetch,
            publisher=await resources.nwstg_publisher(),
            subscription_id=resources.config.converters.sigmet.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.sigmet.is_enabled


class SigmetExtractionHandler(ExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            extractor=await resources.extractor('SIGMET'),
            file_link_id='xml',
            prefetch=resources.config.extractors.sigmet.prefetch,
            subscription_id=resources.config.extractors.sigmet.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.sigmet.is_enabled
