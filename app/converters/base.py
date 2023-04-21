from __future__ import annotations

from abc import ABC, abstractmethod
import inspect
from typing import Optional, Sequence, TYPE_CHECKING

from app.geolocation import ObsStationLocator
from ngitws.types import MediaType

if TYPE_CHECKING:
    from app.resources import ResourceManager


class ConversionInput:
    """Input to a converter."""

    def __init__(self, data: bytes, media_type: MediaType, *, id: str = None):
        self.__data = data
        self.__id = id
        self.__media_type = media_type

    @property
    def data(self) -> bytes:
        """Return the data to convert."""
        return self.__data

    @property
    def id(self) -> Optional[str]:
        """Return an identifier for the input."""
        return self.__id

    @property
    def media_type(self) -> MediaType:
        """Return the data's media type, as described in IETF RFC 6838."""
        return self.__media_type


class ConversionResult:
    """The result of a conversion operation."""

    def __init__(self, data: bytes, media_type: MediaType, *, id: str = None):
        self.__data = data
        self.__id = id
        self.__media_type = media_type

    @property
    def data(self) -> bytes:
        """Return the converted data."""
        return self.__data

    @property
    def id(self) -> Optional[str]:
        """Return an identifier for the result."""
        return self.__id

    @property
    def media_type(self) -> MediaType:
        """Return the data's media type, as described in IETF RFC 6838."""
        return self.__media_type


class Converter(ABC):
    """Base class for data converters."""

    @classmethod
    async def create(cls, resources: ResourceManager) -> Converter:
        return cls()

    @classmethod
    def description(cls) -> str:
        """Return a description of the converter."""
        doc = inspect.getdoc(cls)
        if doc is None:
            raise RuntimeError(f'Missing docstring for {cls.__name__}')

        return doc.partition('\n')[0]

    async def convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        return await self._convert(inputs)

    @abstractmethod
    async def _convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        """Convert one or more inputs to outputs."""


class ObsConverter(Converter):

    def __init__(self, obs_station_locator: ObsStationLocator):
        self.__obs_station_locator = obs_station_locator

    @classmethod
    async def create(cls, resources: ResourceManager) -> Converter:
        return cls(await resources.obs_station_locator())

    @property
    def obs_station_locator(self) -> ObsStationLocator:
        return self.__obs_station_locator

    async def convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        await self.__obs_station_locator.wait_to_populate()

        return await super().convert(inputs)
