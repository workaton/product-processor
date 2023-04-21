from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
import pickle
from types import TracebackType
from typing import Any, Mapping, Optional, Sequence, Type

import aio_msgpack_rpc
from app.converters import ConversionInput, ConversionResult, Converter
from app.extractors import Extractor
from app.handlers import SubscriptionNotificationHandler
from ngitws.catalog import CatalogIdentity
from ngitws.logging import track_correlation
from ngitws.monitoring import Operation
from ngitws.typing import JsonObject


class RpcClient:

    def __init__(self, path: Path):
        self.__client: Optional[aio_msgpack_rpc.Client] = None
        self.__path = path

        self.__logger = logging.getLogger(__name__)

    async def __aenter__(self) -> RpcClient:
        self.__logger.info(f'Connecting to RPC socket at {self.__path}')
        self.__client = aio_msgpack_rpc.Client(*await asyncio.open_unix_connection(str(self.__path)))

        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> None:
        pass

    async def call(self, command_name, *args, **kwargs) -> Any:
        assert self.__client is not None
        func_args = [pickle.dumps(arg) for arg in args]
        func_kwargs = {pickle.dumps(k): pickle.dumps(v) for k, v in kwargs.items()}
        return pickle.loads(await self.__client.call(command_name, *func_args, **func_kwargs))

    async def list_converters(self) -> Mapping[str, str]:
        return await self.call('list_converters')

    async def list_extractors(self) -> Mapping[str, str]:
        return await self.call('list_extractors')

    async def list_handlers(self) -> Mapping[str, str]:
        return await self.call('list_handlers')

    async def run_converter(self, converter_name: str, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        return await self.call('run_converter', converter_name, inputs)

    async def run_extractor(self, extractor_name: str, data: bytes) -> JsonObject:
        return await self.call('run_extractor', extractor_name, data)

    async def run_handler(self, handler_name: str, identity: CatalogIdentity, operation: Operation) -> None:
        return await self.call('run_handler', handler_name, identity, operation)


class RpcServer:

    def __init__(
        self,
        path: Path,
        converters: Mapping[str, Converter],
        extractors: Mapping[str, Extractor],
        handlers: Mapping[str, SubscriptionNotificationHandler]
    ):
        self.__converters = converters
        self.__extractors = extractors
        self.__handlers = handlers
        self.__path = path
        self.__server: Optional[asyncio.AbstractServer] = None

        self.__logger = logging.getLogger(__name__)

    async def __aenter__(self) -> RpcServer:
        self.__logger.info(f'Setting up RPC socket at {self.__path}')
        commands = RpcServerCommands(
            converters=self.__converters,
            extractors=self.__extractors,
            handlers=self.__handlers
        )
        self.__server = await asyncio.start_unix_server(aio_msgpack_rpc.Server(commands), str(self.__path))
        await asyncio.get_running_loop().run_in_executor(None, os.chmod, self.__path, 0o660)

        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> None:
        if self.__server:
            try:
                self.__server.close()
                await self.__server.wait_closed()
            except Exception as ex:
                self.__logger.exception(f'Failed to close RPC server: {str(ex)}')
            self.__server = None
            await asyncio.get_running_loop().run_in_executor(None, os.unlink, self.__path)

    async def wait_closed(self) -> None:
        if self.__server:
            await self.__server.wait_closed()

    @staticmethod
    def async_pickle(func):
        async def wrapper(self, *args, **kwargs):
            args = [pickle.loads(arg) for arg in args]
            kwargs = {pickle.loads(k): pickle.loads(v) for k, v in kwargs.items()}
            result = await func(self, *args, **kwargs)

            return pickle.dumps(result)

        return wrapper


class RpcServerCommands:

    def __init__(
        self,
        converters: Mapping[str, Converter],
        extractors: Mapping[str, Extractor],
        handlers: Mapping[str, SubscriptionNotificationHandler]
    ):
        self.__converters = converters
        self.__extractors = extractors
        self.__handlers = handlers

        self.__logger = logging.getLogger(__name__)

    @RpcServer.async_pickle
    async def list_converters(self) -> Mapping[str, str]:
        return {name: converter.description() for name, converter in self.__converters.items()}

    @RpcServer.async_pickle
    async def list_extractors(self) -> Mapping[str, str]:
        return {name: extractor.description() for name, extractor in self.__extractors.items()}

    @RpcServer.async_pickle
    async def list_handlers(self) -> Mapping[str, str]:
        return {name: handler.description() for name, handler in self.__handlers.items()}

    @RpcServer.async_pickle
    async def run_converter(self, converter_name: str, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        try:
            converter = self.__converters[converter_name]
        except KeyError:
            raise RuntimeError(f'Could not find an converter of type {converter_name}')

        with track_correlation():
            try:
                return await converter.convert(inputs)
            except Exception as ex:
                self.__logger.exception(f'Unexpected error in converter {converter_name}: {str(ex)}')
                raise

    @RpcServer.async_pickle
    async def run_extractor(self, extractor_name: str, data: bytes) -> JsonObject:
        try:
            extractor = self.__extractors[extractor_name]
        except KeyError:
            raise RuntimeError(f'Could not find an extractor of type {extractor_name}')

        with track_correlation():
            try:
                return await extractor.extract(data)
            except Exception as ex:
                self.__logger.exception(f'Unexpected error in extractor {extractor_name}: {str(ex)}')
                raise

    @RpcServer.async_pickle
    async def run_handler(self, handler_name: str, identity: CatalogIdentity, operation: Operation) -> None:
        try:
            handler = self.__handlers[handler_name]
        except KeyError:
            raise RuntimeError(f'Could not find an handler of type {handler_name}')

        with track_correlation():
            try:
                return await handler.run(identity, operation)
            except Exception as ex:
                self.__logger.exception(f'Unexpected error in handler {handler_name}: {str(ex)}')
                raise
