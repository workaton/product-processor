from __future__ import annotations

from abc import ABC, abstractmethod
import asyncio
import inspect
import logging
from typing import Collection, Optional, Sequence, TYPE_CHECKING
import uuid

from aiohttp.client_exceptions import ClientPayloadError
from app.converters import ConversionInput, Converter
from app.exception import InvalidProductError
from app.extractors import Extractor
from app.media_types import MediaTypes
from app.publisher import NwstgPublisher
from ngitws.catalog import CatalogFile, CatalogIdentity, CatalogRecord, CatalogRecordFileMetadata, CatalogRecordStorage
from ngitws.logging import extra_fields, get_correlation_id, get_request_id, is_debug_enabled, track_correlation
from ngitws.monitoring import HealthCheck, HealthCheckResult, Operation, OperationResult, report_operation
from ngitws.time import DateTimeConverter
from ngitws.types import MediaType
from ngitws.typing import JsonObject
from ngitws.web import CatalogWebServiceClient, DataCoherence, WebClientConnectionError, WebClientResponseError
import pendulum

if TYPE_CHECKING:
    from app.resources import ResourceManager


class SubscriptionNotificationHandler(ABC):
    """Base class for job handlers that rely on a RabbitMQ subscription."""

    def __init__(
        self,
        client: CatalogWebServiceClient,
        subscription_id: str,
        health_checks: Collection[HealthCheck] = None,
        *,
        prefetch: Optional[int] = None
    ):
        if health_checks is None:
            health_checks = []

        self.__client = client
        self.__health_checks = tuple(health_checks)
        self.__prefetch = prefetch
        self.__subscription_id = subscription_id

    @classmethod
    def description(cls) -> str:
        """Return a description of the extractor."""
        doc = inspect.getdoc(cls)
        if doc is None:
            raise RuntimeError(f'Missing docstring for {cls.__name__}')

        return doc.partition('\n')[0]

    @classmethod
    @abstractmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        pass

    @classmethod
    @abstractmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        pass

    @property
    def client(self) -> CatalogWebServiceClient:
        return self.__client

    @property
    def obsolete_fields(self) -> Sequence[str]:
        """Return a sequence of names of obsolete fields to remove from records."""
        return ['Content-Type', 'Product-Category', 'Product-Format']

    @property
    def prefetch(self) -> Optional[int]:
        return self.__prefetch

    @property
    def subscription_id(self) -> str:
        return self.__subscription_id

    async def check_health(self) -> Collection[HealthCheckResult]:
        return await asyncio.gather(*[check.run() for check in self.__health_checks])

    async def run(self, identity: CatalogIdentity, operation: Operation) -> None:
        """Run the handler on a given record."""
        try:
            return await self._run(identity, operation)
        except ClientPayloadError as ex:
            operation.error = ex
            operation.message = f'Failed to read response payload while handling {identity}'
            operation.result = OperationResult.DEFER
        except WebClientConnectionError as ex:
            operation.error = ex
            operation.message = f'Web request failed while handling {identity}'
            operation.result = OperationResult.DEFER
        except WebClientResponseError as ex:
            operation.error = ex
            if ex.status == 502:
                operation.message = f'Gateway error while handling {identity}'
                operation.result = OperationResult.DEFER
            if ex.status == 503:
                operation.message = f'Web resource unavailable while handling {identity}'
                operation.result = OperationResult.DEFER
            else:
                operation.message = f'Web request failed ({ex.status}) while handling {identity}'
                operation.result = OperationResult.FAIL
        except Exception as ex:
            operation.error = ex
            operation.message = f'Processing failed unexpectedly while handling {identity}'
            operation.result = OperationResult.FAIL

    @abstractmethod
    async def _run(self, identity: CatalogIdentity, operation: Operation) -> None:
        """Run the handler on a given record."""
        pass

    def _standardize_record(self, record: CatalogRecord, remove_fields: Optional[Sequence[str]] = None):
        """Remove obsolete fields and object identities from a record."""
        if remove_fields is None:
            remove_fields = self.obsolete_fields

        if record.document:
            document = dict(record.document)
            for field in remove_fields:
                document.pop(field, None)
            record = record.with_document(document)
        if record.storage:
            storage = record.storage.with_object_id(None)
            record = record.with_storage(storage)

        return record

    def _timestamp_record(self, record: CatalogRecord, timestamp: Optional[pendulum.DateTime] = None) -> CatalogRecord:
        """Add a processed timestamp to the record for this subscription."""
        if not timestamp:
            timestamp = pendulum.now('UTC')

        document = dict(record.document or {})
        if 'processed' not in document:
            document['processed'] = {}
        document['processed'][self.subscription_id] = DateTimeConverter().write_as_string(timestamp)

        return record.with_document(document)

    async def _upsert_record(
        self,
        identity: CatalogIdentity,
        record: CatalogRecord,
        additional_metadata: Optional[JsonObject] = None
    ) -> CatalogIdentity:
        """Create an updated metadata record to replace the old one."""
        if additional_metadata:
            record = record.with_document({**(record.document or {}), **additional_metadata})
        record = self._timestamp_record(record)

        return await self.__client.catalog(identity.catalog_id).upsert_record(record.id, record)


class ConversionHandler(SubscriptionNotificationHandler):
    """Base class for handlers that convert a file from one format to another.

    Metadata is written back to the originating catalog, replacing the old
    record entirely rather than patching it so a pubsub event is generated.

    Subclasses may override the _update_metadata_record() method to make custom
    modifications to the updated metadata record.  However, it's advised to call
    the method in the superclass to ensure that the target link is added to the
    record.

    """

    def __init__(
        self,
        client: CatalogWebServiceClient,
        converter: Converter,
        file_catalog_id: str,
        subscription_id: str,
        prefetch: Optional[int] = None,
        publisher: NwstgPublisher = None,
        source_link_id: str = 'tac',
        target_link_id: str = 'xml'
    ):
        """Create a new conversion handler.

        :param client: the client for accessing the catalog web service
        :param converter: the converter for changing the file format
        :param subscription_id: the pubsub subscription ID to listen to
        :param file_catalog_id: the catalog to use for new files created
        :param file_link_id: the name of the link to follow to fetch the input file

        """
        super().__init__(client, subscription_id, prefetch=prefetch)
        self.__converter = converter
        self.__file_catalog_id = file_catalog_id
        self.__publisher = publisher
        self.__source_link_id = source_link_id
        self.__target_link_id = target_link_id

        self.__logger = logging.getLogger(__name__)

    @property
    def converter(self) -> Converter:
        return self.__converter

    async def _run(self, identity: CatalogIdentity, operation: Operation) -> None:
        metadata_record = await self.client.get_record(identity, coherence=DataCoherence.CONSISTENT)
        # Check Storage.Object-Identities for backward compatibility
        if self.__source_link_id not in metadata_record.links and len(metadata_record.storage.object_ids) > 0:
            file_identity = metadata_record.storage.object_ids[0]
            metadata_record = metadata_record.with_link(self.__source_link_id, file_identity)

        # Remove obsolete fields
        metadata_record = self._standardize_record(metadata_record)

        extra = {}
        wmo_id = metadata_record.document.get('Wmo-Id')
        if wmo_id is not None:
            extra['wmo_id'] = wmo_id
        office_id = metadata_record.document.get('Issuing-Office')
        if office_id is not None:
            extra['office_id'] = office_id

        try:
            conversion_input = await self._get_input_data(identity, metadata_record)
            conversion_results = await self.__converter.convert(conversion_input)
            if len(conversion_results) == 0:
                # When the converter returns nothing, count that as a skip.
                operation.message = f'{self.__converter.__class__.__name__} returned no result'
                operation.result = OperationResult.SKIP
                return

            conversion_result = conversion_results[0]
            converted_file_record_id = self._create_converted_record_id(identity, metadata_record)
            converted_file_id = CatalogIdentity(self.__file_catalog_id, converted_file_record_id)

            converted_file = CatalogFile(CatalogRecord(
                storage=CatalogRecordStorage(record_id=converted_file_record_id),
                file_metadata=CatalogRecordFileMetadata(content_type=conversion_result.media_type)
            ), conversion_result.data)
            result_file_id = await self.client.catalog(self.__file_catalog_id).create_file(converted_file)
            if result_file_id != converted_file_id:
                raise RuntimeError(
                    f'Returned file record ID {result_file_id} did not match request {converted_file_id}'
                )
            self.__logger.info(f'Created converted {conversion_result.media_type} file {converted_file_id}')

            metadata_record = await self._update_metadata_record(metadata_record, converted_file_id)
            metadata_id = await self._upsert_record(identity, metadata_record)
            if metadata_id != identity:
                raise RuntimeError(f'Returned metadata record ID {metadata_id} did not match request {identity}')

            if self.__publisher:
                try:
                    await self.__publisher.request(
                        identity,
                        converted_file_id,
                        issuance_time=DateTimeConverter().read_as_datetime(metadata_record.document['Issue-Time']),
                        issuing_office=metadata_record.document['Issuing-Office'],
                        wmo_id=await self._get_publisher_wmo_id(metadata_record.document['Wmo-Id'])
                    )
                except KeyError as ex:
                    self.__logger.exception(
                        f'Failed to schedule file {converted_file_id} for NWSTG publishing: missing field {str(ex)}'
                    )

            operation.message = f'Conversion completed for {identity}'
            operation.result = OperationResult.PASS
        finally:
            for name, value in extra.items():
                operation.set_extra(name, value)

    def _create_converted_record_id(self, metadata_id: CatalogIdentity, metadata_record: CatalogRecord) -> str:
        return str(uuid.uuid4())

    async def _get_input_data(
        self,
        identity: CatalogIdentity,
        metadata_record: CatalogRecord
    ) -> Sequence[ConversionInput]:
        if self.__source_link_id not in metadata_record.links:
            raise InvalidProductError(f'Missing {self.__source_link_id} file link in {identity}')

        file_identity = metadata_record.links[self.__source_link_id]

        async with self.client.get_file(file_identity, coherence=DataCoherence.CONSISTENT) as file_record:
            source_content_type = file_record.record.file_metadata.content_type
            file_data = b''.join([chunk async for chunk in file_record.data])

            return [ConversionInput(file_data, source_content_type)]

    async def _get_publisher_wmo_id(self, wmo_id: str) -> str:
        return f'L{wmo_id[1:]}'

    async def _update_metadata_record(self, record: CatalogRecord, file_id: CatalogIdentity) -> CatalogRecord:
        return record.with_link(self.__target_link_id, file_id)


class CollectiveExtractionHandler(SubscriptionNotificationHandler):
    """Base class for handlers that split and extract metadata from collectives.

    The split files and metadata are written to new catalogs.  The new metadata records each have a "collective" link
    back to the original collective record.

    Subclasses may override the _create_metadata_record() method to make further
    modifications to the new metadata record.

    """

    NOTIFICATION_HANDLER_PART_OPERATION_ID = 'handle_notification_part'

    def __init__(
        self,
        client: CatalogWebServiceClient,
        extractor: Extractor,
        subscription_id: str,
        collective_file_link_id: str,
        part_metadata_catalog_id: str,
        part_file_catalog_id: Optional[str] = None,
        part_file_link_id: Optional[str] = None,
        prefetch: Optional[int] = None,
        part_media_type: MediaType = MediaTypes.APPLICATION_OCTET_STREAM
    ):
        """Create a new collective extraction handler.

        :param client: the client for accessing the catalog web service
        :param extractor: the extractor for gathering metadata
        :param part_file_catalog_id: the catalog for new files created
        :param part_metadata_catalog_id: the catalog for extracted metadata
        :param subscription_id: the pubsub subscription ID to listen to

        """
        super().__init__(client, subscription_id, prefetch=prefetch)
        self.__extractor = extractor
        self.__file_catalog_id = part_file_catalog_id
        self.__metadata_catalog_id = part_metadata_catalog_id
        self.__part_file_link_id = part_file_link_id
        self.__part_media_type = part_media_type
        self.__source_link_id = collective_file_link_id

        self.__logger = logging.getLogger(__name__)

    @property
    def extractor(self) -> Extractor:
        return self.__extractor

    @property
    def obsolete_fields(self) -> Sequence[str]:
        return list(super().obsolete_fields) + ['Feed-Type']

    async def _run(self, identity: CatalogIdentity, operation: Operation) -> None:
        collective_record = await self.client.get_record(identity, coherence=DataCoherence.CONSISTENT)
        collective_record = await self._update_collective_record(identity, collective_record)

        if self.__source_link_id not in collective_record.links:
            raise InvalidProductError(f'Missing {self.__source_link_id} file link in {identity}')
        collective_file_id = collective_record.links[self.__source_link_id]

        await self._upsert_record(identity, collective_record)

        async with self.client.get_file(collective_file_id, coherence=DataCoherence.CONSISTENT) as collective_file:
            collective_data = b''.join([chunk async for chunk in collective_file.data])
        parts = await self._split_collective_data(collective_data)
        self.__logger.debug(f'Found {len(parts)} individual product(s) in {identity}')

        tasks = [self._handle_part(part, identity, collective_record) for part in parts]
        results: Sequence[OperationResult] = await asyncio.gather(*tasks)
        defer_results = sum([1 for result in results if result == OperationResult.DEFER])
        fail_results = sum([1 for result in results if result == OperationResult.FAIL])
        extra = {
            'defer_count': defer_results,
            'fail_count': fail_results,
            'product_count': len(parts)
        }

        if fail_results:
            operation.message = \
                f'Processing failed for {fail_results} parts ' \
                f'(deferred for {defer_results} parts) ' \
                f'of collective product {identity}'
            operation.result = OperationResult.FAIL
        elif defer_results:
            operation.message = f'Collective extraction deferred for {defer_results} parts of {identity}'
            operation.result = OperationResult.DEFER
        else:
            operation.message = f'Collective extraction completed for {identity}'
            operation.result = OperationResult.PASS

        for name, value in extra.items():
            operation.set_extra(name, value)

    async def _create_part_record(
        self,
        part_identity: CatalogIdentity,
        collective_identity: CatalogIdentity,
        collective_record: CatalogRecord,
        extracted_metadata: JsonObject
    ) -> CatalogRecord:
        """Create a metadata record for each part of the collective."""
        part_document = {**(collective_record.document or {}), **extracted_metadata}
        if 'processed' in part_document:
            del part_document['processed']

        return CatalogRecord(
            storage=CatalogRecordStorage(record_id=part_identity.record_id),
            document=part_document,
            links={'collective': collective_identity}
        )

    async def _handle_part(
        self,
        data: bytes,
        collective_identity: CatalogIdentity,
        collective_record: CatalogRecord
    ) -> OperationResult:
        with extra_fields({'super_correlation_id': get_correlation_id()}):
            with track_correlation(request_id=get_request_id()):
                with report_operation(self.NOTIFICATION_HANDLER_PART_OPERATION_ID) as operation:
                    operation.set_extra('collective_catalog_id', collective_identity.catalog_id)
                    operation.set_extra('collective_record_id', collective_identity.record_id)
                    try:
                        extracted_metadata = await self.__extractor.extract(data)
                        if is_debug_enabled():
                            self.__logger.debug(f'Extracted metadata from part: {extracted_metadata}')

                        part_record_id = self._create_part_record_id(
                            collective_identity,
                            collective_record,
                            extracted_metadata
                        )
                        part_record_identity = CatalogIdentity(self.__metadata_catalog_id, part_record_id)
                        part_record = await self._create_part_record(
                            part_record_identity,
                            collective_identity,
                            collective_record,
                            extracted_metadata
                        )

                        # Upload the file fragment if a file link ID was set on this handler.
                        if self.__part_file_link_id:
                            part_file_identity = CatalogIdentity(self.__file_catalog_id, part_record_id)

                            file_record = CatalogRecord(
                                storage=CatalogRecordStorage(record_id=part_record_id),
                                file_metadata=CatalogRecordFileMetadata(content_type=self.__part_media_type)
                            )
                            part_file = CatalogFile(file_record, data)
                            await self.client.catalog(self.__file_catalog_id).create_file(part_file)

                            part_record = part_record.with_link(self.__part_file_link_id, part_file_identity)

                        await self._upsert_record(part_record_identity, part_record)

                        operation.message = \
                            f'Processing completed for part from collective product {collective_identity}'
                        operation.result = OperationResult.PASS
                    # Adapted from NotificationConsumer
                    except WebClientConnectionError as ex:
                        operation.result = OperationResult.DEFER
                        operation.message = \
                            f'Web request failed while handling part from collective product {collective_identity}'
                        operation.error = ex
                    except WebClientResponseError as ex:
                        operation.error = ex
                        if ex.status == 502:
                            operation.result = OperationResult.DEFER
                            operation.message = \
                                f'Gateway error while handling part from collective product {collective_identity}'
                        if ex.status == 503:
                            operation.result = OperationResult.DEFER
                            operation.message = \
                                f'Resource unavailable while handling part from collective product ' \
                                f'{collective_identity}'
                        else:
                            operation.result = OperationResult.FAIL
                            operation.message = \
                                f'Web request failed ({ex.status}) while handling part from collective product ' \
                                f'{collective_identity}'
                    except Exception as ex:
                        operation.result = OperationResult.FAIL
                        operation.message = \
                            f'Failed to extract metadata for entry from collective product {collective_identity}'
                        operation.error = ex

                    return operation.result

    def _create_part_record_id(
        self,
        collective_id: CatalogIdentity,
        collective_record: CatalogRecord,
        extracted_metadata: JsonObject
    ) -> str:
        return str(uuid.uuid4())

    @abstractmethod
    async def _split_collective_data(self, data: bytes) -> Sequence[bytes]:
        pass

    async def _update_collective_record(
            self,
            collective_identity: CatalogIdentity,
            collective_record: CatalogRecord
    ) -> CatalogRecord:
        """Update the metadata record for the collective."""
        # Check Storage.Object-Identities for backward compatibility
        if self.__source_link_id not in collective_record.links and len(collective_record.storage.object_ids) > 0:
            collective_file_id = collective_record.storage.object_ids[0]
            collective_record = collective_record.with_link(self.__source_link_id, collective_file_id)

        # Remove obsolete fields
        collective_record = self._standardize_record(collective_record)

        return collective_record


class ExtractionHandler(SubscriptionNotificationHandler):
    """Handler for extracting metadata from products.

    Metadata is written back to the originating catalog, replacing the old
    record entirely rather than patching it so a pubsub event is generated.

    Subclasses may override the _update_metadata_record() method to make further
    modifications to the updated metadata record.

    """

    def __init__(
        self,
        client: CatalogWebServiceClient,
        extractor: Extractor,
        subscription_id: str,
        file_link_id: str,
        prefetch: Optional[int] = None,
    ):
        """Create a new extraction handler.

        :param client: the client for accessing the catalog web service
        :param extractor: the extractor for gathering metadata
        :param file_link_id: the metadata record link ID for the source file
        :param subscription_id: the pubsub subscription ID to listen to

        """
        super().__init__(client, subscription_id, prefetch=prefetch)
        self.__extractor = extractor
        self.__file_link_id = file_link_id

        self.__logger = logging.getLogger(__name__)

    @property
    def extractor(self) -> Extractor:
        return self.__extractor

    async def _run(self, identity: CatalogIdentity, operation: Operation) -> None:
        metadata_record = await self.client.get_record(identity, coherence=DataCoherence.CONSISTENT)
        file_identity = metadata_record.links.get(self.__file_link_id)

        # Check Storage.Object-Identities for backward compatibility
        if not file_identity:
            if len(metadata_record.storage.object_ids) == 0:
                raise InvalidProductError(f'Missing {self.__file_link_id} file link in {identity}')
            file_identity = metadata_record.storage.object_ids[0]
            metadata_record = metadata_record.with_link(self.__file_link_id, file_identity)

        # Remove obsolete fields
        metadata_record = self._standardize_record(metadata_record)

        async with self.client.get_file(file_identity, coherence=DataCoherence.CONSISTENT) as file_record:
            file_data = b''.join([chunk async for chunk in file_record.data])

        extracted_metadata = await self.__extractor.extract(file_data)
        await self._upsert_record(identity, metadata_record, extracted_metadata)

        operation.message = f'Extraction completed for {identity}'
        operation.result = OperationResult.PASS
