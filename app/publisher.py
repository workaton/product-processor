from __future__ import annotations

import logging
from typing import Dict

import aiofiles
import aiofiles.os
from app.exception import InvalidProductError
from ngitws.catalog import CatalogIdentity, CatalogRecord
from ngitws.time import DateTimeConverter
from ngitws.web import CatalogWebServiceClient, DataCoherence
import pendulum


class NwstgPublisher:
    """Helper to post records for the NWSTG handler to publish."""

    FILE_LINK_ID = 'file'
    METADATA_LINK_ID = 'metadata'

    ISSUANCE_TIME_FIELD = 'Issue-Time'
    ISSUING_OFFICE_ID_FIELD = 'Issuing-Office'
    PUBLISHED_FILENAME = 'Published-Filename'
    PUBLISHED_TIMESTAMP = 'Published-Time'
    WMO_ID_FIELD = 'Wmo-Id'

    def __init__(self, client: CatalogWebServiceClient, publisher_catalog_id: str, base_path: str):
        self.__base_path = base_path
        self.__catalog_id = publisher_catalog_id
        self.__client = client
        self.__stations: Dict[str, str] = {}

        self.__logger = logging.getLogger(__name__)

    async def request(
        self,
        metadata_identity: CatalogIdentity,
        file_identity: CatalogIdentity,
        issuance_time: pendulum.DateTime,
        issuing_office: str,
        wmo_id: str
    ) -> CatalogIdentity:
        record = CatalogRecord(
            document={
                self.ISSUANCE_TIME_FIELD: DateTimeConverter().write_as_string(issuance_time),
                self.ISSUING_OFFICE_ID_FIELD: issuing_office,
                self.WMO_ID_FIELD: wmo_id
            },
            links={
                self.METADATA_LINK_ID: metadata_identity,
                self.FILE_LINK_ID: file_identity
            }
        )

        return await self.__client.catalog(self.__catalog_id).create_record(record)

    async def publish(self, identity: CatalogIdentity) -> NwstgPublisherResult:
        record = await self.__client.get_record(identity, coherence=DataCoherence.CONSISTENT)

        if self.METADATA_LINK_ID not in record.links:
            raise InvalidProductError(f'Record does not contain {self.METADATA_LINK_ID} link')
        if self.FILE_LINK_ID not in record.links:
            raise InvalidProductError(f'Record does not contain {self.FILE_LINK_ID} link')
        metadata_identity = record.links[self.METADATA_LINK_ID]
        file_identity = record.links[self.FILE_LINK_ID]

        filename = self.__get_filename(metadata_identity, record)
        path = f'{self.__base_path}/{filename}'
        temp_path = f'{self.__base_path}/.{filename}'
        wmo_header = self.__get_wmo_header(record).encode() + b'\r\r\n'

        async with self.__client.get_file(file_identity, coherence=DataCoherence.CONSISTENT) as catalog_file:
            self.__logger.info(f'Publishing {file_identity} (from {identity}) to {path}')

            async with aiofiles.open(temp_path, 'wb') as output_file:
                await output_file.write(wmo_header)
                async for chunk in catalog_file.data:
                    await output_file.write(chunk)

        self.__logger.debug(f'Moving {temp_path} to {path}')
        await aiofiles.os.rename(temp_path, path)
        published_time = pendulum.now('UTC')

        record = record.with_document({**record.document, **{
            'Published-Filename': filename,
            'Published-Time': DateTimeConverter().write_as_string(published_time)
        }})

        await self.__client.upsert_record(identity, record)

        return self.NwstgPublisherResult(filename, path, published_time)

    def __get_filename(self, identity: CatalogIdentity, record: CatalogRecord) -> str:
        filename = f'{identity.catalog_id}.{identity.record_id}'
        if record.storage.last_correlation_id:
            filename = f'{filename}.{record.storage.last_correlation_id}'

        return filename

    def __get_wmo_header(self, record: CatalogRecord) -> str:
        wmo_id = record.document.get(self.WMO_ID_FIELD)
        office_id = record.document.get(self.ISSUING_OFFICE_ID_FIELD)
        issuance_time = DateTimeConverter().read_as_datetime(record.document.get(self.ISSUANCE_TIME_FIELD))

        if not wmo_id:
            raise RuntimeError(f'Failed to find "{self.WMO_ID_FIELD}" field in metadata record')
        if not office_id:
            raise RuntimeError(f'Failed to find "{self.ISSUING_OFFICE_ID_FIELD}" field in metadata record')
        if not issuance_time:
            raise RuntimeError(f'Failed to find "{self.ISSUANCE_TIME_FIELD}" field in metadata record')

        return f'{wmo_id} {office_id} {issuance_time.format("DDHHmm")}'

    class NwstgPublisherResult:
        """The result of a successful publishing operation."""

        def __init__(self, filename: str, path: str, timestamp: pendulum.DateTime):
            self.__filename = filename
            self.__path = path
            self.__timestamp = timestamp

        @property
        def filename(self) -> str:
            return self.__filename

        @property
        def path(self) -> str:
            return self.__path

        @property
        def timestamp(self) -> pendulum.DateTime:
            return self.__timestamp
