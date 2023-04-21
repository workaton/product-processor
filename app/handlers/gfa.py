from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ConversionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class GfaConversionHandler(ConversionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('GFA'),
            file_catalog_id=resources.config.converters.gfa.file_catalog_id,
            prefetch=resources.config.converters.gfa.prefetch,
            source_link_id='g3fax',
            subscription_id=resources.config.converters.gfa.subscription_id,
            target_link_id='png'
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.gfa.is_enabled
