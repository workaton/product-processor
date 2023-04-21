from __future__ import annotations

import json
from typing import Sequence, TYPE_CHECKING

from app.converters import ConversionInput
from app.media_types import MediaTypes
from app.util.splitter import LineSplitter
from ngitws.catalog import CatalogIdentity, CatalogRecord

from .base import CollectiveExtractionHandler, ConversionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class MadisJsonConversionHandler(ConversionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('MADIS-JSON'),
            file_catalog_id=resources.config.converters.madis.file_catalog_id,
            prefetch=resources.config.converters.madis.prefetch,
            source_link_id='csv',
            subscription_id=resources.config.converters.madis.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.madis.is_enabled

    async def _get_input_data(
        self,
        identity: CatalogIdentity,
        metadata_record: CatalogRecord
    ) -> Sequence[ConversionInput]:
        madis_data = json.dumps(metadata_record.document).encode()

        return [ConversionInput(madis_data, MediaTypes.APPLICATION_JSON)]


class MadisCsvExtractionHandler(CollectiveExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            collective_file_link_id='csv',
            extractor=await resources.extractor('MADIS-CSV'),
            part_metadata_catalog_id=resources.config.extractors.madis.metadata_catalog_id,
            part_media_type=MediaTypes.TEXT_CSV,
            prefetch=resources.config.extractors.madis.prefetch,
            subscription_id=resources.config.extractors.madis.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.madis.is_enabled

    async def _split_collective_data(self, data: bytes) -> Sequence[bytes]:
        return await LineSplitter().split(data.strip())
