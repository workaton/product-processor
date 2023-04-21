from __future__ import annotations

from contextlib import asynccontextmanager, AsyncExitStack
from pathlib import Path
from types import TracebackType
from typing import AsyncGenerator, Optional, Type

from app.converters import Converter, CONVERTERS
from app.extractors import Extractor, EXTRACTORS
from app.spot import StqApp, SPOT
from app.handlers import HANDLERS, SubscriptionNotificationHandler
from ngitws.asyncio import Scheduler
from ngitws.rabbitmq import AmqpConnectionParameters
from ngitws.rabbitmq.notification import NotificationSubscriber
from ngitws.web import CatalogWebServiceClient, SubscriptionWebServiceClient
import pendulum

from .config import Configuration
from .geolocation import ObsStationLocator
from .publisher import NwstgPublisher
from .rpc import RpcServer


class ResourceManager:
    """Manager for resources used in the application."""

    def __init__(self, config: Configuration):
        self.__config = config
        self.__stack: Optional[AsyncExitStack] = None

        self.__catalog_client: Optional[CatalogWebServiceClient] = None
        self.__nwstg_publisher: Optional[NwstgPublisher] = None
        self.__obs_station_locator: Optional[ObsStationLocator] = None
        self.__subscription_client: Optional[SubscriptionWebServiceClient] = None

    async def __aenter__(self) -> ResourceManager:
        if self.__stack:
            raise RuntimeError('ResourceManager is already open')
        self.__stack = AsyncExitStack()
        await self.__stack.__aenter__()

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        try:
            if self.__stack:
                await self.__stack.__aexit__(None, None, None)
        finally:
            self.__catalog_client = None
            self.__obs_station_locator = None
            self.__nwstg_publisher = None
            self.__subscription_client = None
            self.__stack = None

    @property
    def config(self) -> Configuration:
        """Return the application configuration."""
        return self.__config

    async def converter(self, name: str) -> Converter:
        """Return a converter instance or raise an exception if not available."""
        return await CONVERTERS[name].create(self)

    async def extractor(self, name: str) -> Extractor:
        """Return an extractor instance or raise an exception if not available."""
        return await EXTRACTORS[name].create(self)

    async def handler(self, name: str) -> SubscriptionNotificationHandler:
        """Return a subscription handler instance or raise an exception if not available."""
        return await HANDLERS[name].create(self)

    async def catalog_client(self) -> CatalogWebServiceClient:
        if not self.__stack:
            raise RuntimeError('ResourceManager is not open')

        if not self.__catalog_client:
            self.__catalog_client = await self.__stack.enter_async_context(CatalogWebServiceClient.create(
                auth=(self.__config.catalog_username, self.__config.catalog_password),
                base_url=self.__config.catalog_url
            ))

        return self.__catalog_client

    async def nwstg_publisher(self) -> NwstgPublisher:
        if not self.__stack:
            raise RuntimeError('ResourceManager is not open')

        if not self.__nwstg_publisher:
            client = await self.catalog_client()
            self.__nwstg_publisher = NwstgPublisher(
                client,
                self.__config.nwstg_publisher.catalog_id,
                self.__config.nwstg_publisher.base_path
            )

        return self.__nwstg_publisher

    async def obs_station_locator(self) -> ObsStationLocator:
        """Return an instance of the obs station cache."""
        if not self.__stack:
            raise RuntimeError('ResourceManager is not open')

        if not self.__obs_station_locator:
            duration = pendulum.duration(seconds=self.__config.ob_stations_refresh)
            client = await self.catalog_client()
            locator = ObsStationLocator(client.catalog(self.__config.ob_stations_catalog_id))
            await self.__stack.enter_async_context(Scheduler(locator.populate_data).repeat(duration))
            self.__obs_station_locator = locator

        return self.__obs_station_locator

    async def subscription_client(self) -> SubscriptionWebServiceClient:
        if not self.__stack:
            raise RuntimeError('ResourceManager is not open')

        if not self.__subscription_client:
            self.__subscription_client = await self.__stack.enter_async_context(SubscriptionWebServiceClient.create(
                auth=(self.__config.pubsub.subws_username, self.__config.pubsub.subws_password),
                base_url=self.__config.pubsub.subws_url
            ))

        return self.__subscription_client

    @asynccontextmanager
    async def run_notification_subscriber(self) -> AsyncGenerator[NotificationSubscriber, None]:
        async with NotificationSubscriber(
            amqp_parameters=[AmqpConnectionParameters(amqp_url) for amqp_url in self.__config.pubsub.amqp_urls],
            name='products',
            prefetch=self.__config.pubsub.prefetch,
            subws_client=await self.subscription_client()
        ) as subscriber:
            yield subscriber

    @asynccontextmanager
    async def run_rpc_server(self, socket_path: Path) -> AsyncGenerator[RpcServer, None]:
        converters = {k: await v.create(self) for k, v in CONVERTERS.items()}
        extractors = {k: await v.create(self) for k, v in EXTRACTORS.items()}
        handlers = {k: await v.create(self) for k, v in HANDLERS.items() if v is not None}

        async with RpcServer(socket_path, converters, extractors, handlers) as rpc_server:
            yield rpc_server
