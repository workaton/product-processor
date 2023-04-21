from __future__ import annotations

import asyncio
from contextlib import AsyncExitStack
import logging
from pathlib import Path
from types import TracebackType
from typing import Optional, Sequence, Type

from app.handlers import HANDLERS
from ngitws.monitoring import Operation
from ngitws.rabbitmq.notification import Notification, NotificationSubscriber
from ngitws.subscription import SubscriptionNotFoundError

from .config import Configuration
from .handlers import SubscriptionNotificationHandler
from .resources import ResourceManager


class Daemon:

    def __init__(self, config: Configuration, pubsub: bool, socket_path: Path, handlers: Sequence[str]):
        self.__config = config
        self.__handlers = handlers
        self.__pubsub = pubsub
        self.__socket_path = socket_path
        self.__stack: Optional[AsyncExitStack] = None

        self.__logger = logging.getLogger(__name__)

    async def __aenter__(self) -> Daemon:
        if self.__stack:
            raise RuntimeError('Daemon is already open')
        self.__stack = AsyncExitStack()

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        try:
            if self.__stack:
                await self.__stack.aclose()
        finally:
            self.__stack = None

    async def run(self) -> None:
        try:
            async with ResourceManager(self.__config) as resources:
                tasks = []
                tasks.append(asyncio.create_task(self.__run_rpc_server(resources)))
                if self.__pubsub:
                    tasks.append(asyncio.create_task(self.__run_subscriber(resources)))

                self.__logger.debug('Main task waiting for subtasks to exit')
                await asyncio.gather(*tasks)
        except Exception:
            self.__logger.exception('Unexpected error occurred in main task')
        finally:
            self.__logger.info('Exiting main program loop')

    async def __register_handler(
        self,
        subscriber: NotificationSubscriber,
        handler: SubscriptionNotificationHandler
    ) -> None:
        self.__logger.debug(f'Attempting to register handler for {handler.subscription_id}')
        try:
            async def wrapped(notification: Notification, operation: Operation) -> None:
                return await handler.run(notification.identity, operation)

            await subscriber.listen(handler.subscription_id, wrapped)
        except SubscriptionNotFoundError:
            self.__logger.warning(f'Disabling {handler.subscription_id} handler; subscription not found')

    async def __run_rpc_server(self, resources: ResourceManager) -> None:
        while True:
            try:
                async with resources.run_rpc_server(self.__socket_path) as rpc_server:
                    await rpc_server.wait_closed()
            except asyncio.CancelledError:
                break
            except Exception:
                self.__logger.exception('RPC server exited unexpectedly')
            self.__logger.debug('Restarting RPC server')

    async def __run_subscriber(self, resources: ResourceManager) -> None:
        while True:
            try:
                async with resources.run_notification_subscriber() as subscriber:
                    for handler_name in HANDLERS:
                        if self.__handlers and handler_name not in self.__handlers:
                            continue
                        await self.__register_handler(subscriber, await resources.handler(handler_name))
                    await subscriber.wait_closed()
            except asyncio.CancelledError:
                break
            except Exception:
                self.__logger.exception('Notification subscriber exited unexpectedly')
            self.__logger.debug('Restarting notification subscriber')
