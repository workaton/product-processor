from __future__ import annotations

import asyncio
import logging
from typing import Optional, TYPE_CHECKING

from app.converters import ConversionInput, Converter
from app.exception import InvalidProductError
from app.media_types import MediaTypes
from ngitws.catalog import CatalogFile, CatalogIdentity, CatalogRecord, CatalogRecordFileMetadata
from ngitws.monitoring import Operation, OperationResult
from ngitws.web import CatalogWebServiceClient, DataCoherence

from .base import ExtractionHandler, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class SpcWatchConversionHandler(SubscriptionNotificationHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            converter=await resources.converter('SPCWATCH'),
            saw_file_catalog_id=resources.config.converters.spc_watch.saw_file_catalog_id,
            saw_metadata_catalog_id=resources.config.converters.spc_watch.saw_metadata_catalog_id,
            sel_file_catalog_id=resources.config.converters.spc_watch.sel_file_catalog_id,
            sel_metadata_catalog_id=resources.config.converters.spc_watch.sel_metadata_catalog_id,
            prefetch=resources.config.converters.spc_watch.prefetch,
            subscription_id=resources.config.converters.spc_watch.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.spc_watch.is_enabled

    def __init__(
        self,
        client: CatalogWebServiceClient,
        converter: Converter,
        saw_file_catalog_id: str,
        saw_metadata_catalog_id: str,
        sel_file_catalog_id: str,
        sel_metadata_catalog_id: str,
        subscription_id: str,
        prefetch: Optional[int] = None,
        source_link_id: str = 'tac',
        target_link_id: str = 'xml'
    ):
        super().__init__(client, subscription_id, prefetch=prefetch)
        self.__converter = converter
        self.__saw_file_catalog_id = saw_file_catalog_id
        self.__saw_metadata_catalog_id = saw_metadata_catalog_id
        self.__sel_file_catalog_id = sel_file_catalog_id
        self.__sel_metadata_catalog_id = sel_metadata_catalog_id
        self.__source_link_id = source_link_id
        self.__target_link_id = target_link_id

        self.__logger = logging.getLogger(__name__)

    async def _run(self, identity: CatalogIdentity, operation: Operation) -> None:
        metadata_record = await self.client.get_record(identity, coherence=DataCoherence.CONSISTENT)
        document = metadata_record.document
        product_id = document['Product-Identifier']
        issue_time = document['Issue-Time']
        watch_number = document['Watch-Number']

        extra = {'watch_number': watch_number}
        fiql = f'Doc.Issue-Time=={issue_time};Doc.Watch-Number=={watch_number}'

        try:
            if product_id == 'SAW':
                # If SAW, then get SEL
                records = await self.client.catalog(self.__sel_metadata_catalog_id).query_records(
                    f'Doc.Product-Identifier==SEL;{fiql}',
                    limit=1,
                    coherence=DataCoherence.CONSISTENT
                )
                if not records:
                    operation.message = \
                        f'Companion SEL product for {issue_time} (watch number {watch_number}) not available yet'
                    operation.result = OperationResult.SKIP
                    return

                saw_record = metadata_record
                sel_record = records[0]

                saw_identity = identity
                sel_identity = CatalogIdentity(self.__sel_metadata_catalog_id, sel_record.id)
            elif product_id == 'SEL':
                # If SEL, then get SAW
                records = await self.client.catalog(self.__saw_metadata_catalog_id).query_records(
                    f'Doc.Product-Identifier==SAW;{fiql}',
                    limit=1,
                    coherence=DataCoherence.CONSISTENT
                )
                if not records:
                    operation.message = \
                        f'Companion SAW product for {issue_time} (watch number {watch_number}) not available yet'
                    operation.result = OperationResult.SKIP
                    return

                saw_record = records[0]
                sel_record = metadata_record

                saw_identity = CatalogIdentity(self.__saw_metadata_catalog_id, saw_record.id)
                sel_identity = identity
            else:
                # Then what is this?
                raise RuntimeError(f'Received product of unexpected type "{product_id}"')

            # Check whether or not the records should be handled at this time.
            if not self.__should_handle_records(product_id, saw_record, sel_record):
                operation.message = 'Yielding handling to companion product'
                operation.result = OperationResult.SKIP
                return

            # Update SAW/SEL records
            saw_record = self.__update_metadata_record(saw_record, 'sel', sel_identity)
            sel_record = self.__update_metadata_record(sel_record, 'saw', saw_identity)

            # Fetch and convert TAC files
            inputs = await asyncio.gather(
                self.__fetch_input(saw_record.links[self.__source_link_id], 'SAW'),
                self.__fetch_input(sel_record.links[self.__source_link_id], 'SEL')
            )
            converted_results = await self.__converter.convert(inputs)

            for converted in converted_results:
                converted_record = CatalogRecord(
                    file_metadata=CatalogRecordFileMetadata(content_type=MediaTypes.APPLICATION_USWX_XML)
                )
                file = CatalogFile(converted_record, converted.data)
                if converted.id == 'SAW':
                    converted_file_id = await self.client.catalog(self.__saw_file_catalog_id).create_file(file)
                    saw_record = saw_record.with_link(self.__target_link_id, converted_file_id)
                elif converted.id == 'SEL':
                    converted_file_id = await self.client.catalog(self.__sel_file_catalog_id).create_file(file)
                    sel_record = sel_record.with_link(self.__target_link_id, converted_file_id)
                else:
                    # This shouldn't happen
                    raise RuntimeError(f'SPC watch converter returned result with ID of {repr(converted.id)}')

            # Commit SAW/SEL record changes
            await asyncio.gather(
                self._upsert_record(saw_identity, saw_record),
                self._upsert_record(sel_identity, sel_record)
            )

            operation.result = OperationResult.PASS
        finally:
            for name, value in extra.items():
                operation.set_extra(name, value)

    async def __fetch_input(self, identity: CatalogIdentity, product_id: str) -> ConversionInput:
        async with self.client.get_file(identity) as file:
            file_data = b''.join([chunk async for chunk in file.data])
            return ConversionInput(file_data, MediaTypes.TEXT_PLAIN, id=product_id)

    def __should_handle_records(self, product_id: str, saw_record: CatalogRecord, sel_record: CatalogRecord) -> bool:
        # Resolve possible race condition leading to double handling.
        # Handle the records if this product's publish date is later than the other one's.
        # In the unlikely event of a tie, handle if this product is SAW.
        if saw_record.storage.publish_date >= sel_record.storage.publish_date:
            record_to_handle = 'SAW'
        else:
            record_to_handle = 'SEL'

        return product_id == record_to_handle

    def __update_metadata_record(
        self,
        record: CatalogRecord,
        linked_name: str,
        linked_identity: CatalogIdentity
    ) -> CatalogRecord:
        if self.__source_link_id not in record.links:
            # Check Storage.Object-Identities for backward compatibility
            if len(record.storage.object_ids) == 0:
                raise InvalidProductError(f'Missing {self.__source_link_id} file link in {record}')
            file_id = record.storage.object_ids[0]
            record = record.with_link(self.__source_link_id, file_id)

        # Remove obsolete fields
        record = self._standardize_record(record)

        return record.with_link(linked_name, linked_identity)


class SawExtractionHandler(ExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            extractor=await resources.extractor('SAW'),
            file_link_id='xml',
            prefetch=resources.config.extractors.saw.prefetch,
            subscription_id=resources.config.extractors.saw.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.saw.is_enabled


class SelExtractionHandler(ExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            extractor=await resources.extractor('SEL'),
            file_link_id='xml',
            prefetch=resources.config.extractors.sel.prefetch,
            subscription_id=resources.config.extractors.sel.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.sel.is_enabled
