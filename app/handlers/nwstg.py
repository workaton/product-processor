from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING

from app.publisher import NwstgPublisher
from ngitws.catalog import CatalogIdentity
from ngitws.monitoring import Operation, OperationResult
from ngitws.web import CatalogWebServiceClient

from .base import SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class NwstgPublisherHandler(SubscriptionNotificationHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            prefetch=resources.config.nwstg_publisher.prefetch,
            publisher=await resources.nwstg_publisher(),
            subscription_id=resources.config.nwstg_publisher.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.nwstg_publisher.is_enabled

    def __init__(
            self,
            client: CatalogWebServiceClient,
            subscription_id: str,
            publisher: NwstgPublisher,
            prefetch: Optional[int] = None
    ):
        super().__init__(client, subscription_id, prefetch=prefetch)
        self.__publisher = publisher

        self.__logger = logging.getLogger(__name__)

    async def _run(self, identity: CatalogIdentity, operation: Operation) -> None:
        """Run the handler on a given record."""
        result = await self.__publisher.publish(identity)

        operation.message = f'Published {identity} to {result.path}'
        operation.result = OperationResult.PASS
        operation.set_extra('file_path', result.path)
