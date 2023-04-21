from __future__ import annotations

import logging
import asyncio
import aiofiles
import aiofiles.os

from typing import Optional, TYPE_CHECKING

import traceback

from ngitws.catalog import CatalogFile, CatalogIdentity, CatalogRecord, CatalogRecordFileMetadata
from ngitws.monitoring import Operation
from ngitws.web import CatalogWebServiceClient, DataCoherence, CatalogAccessor

from .base import SubscriptionNotificationHandler
from app.media_types import MediaTypes
from app.publisher import NwstgPublisher
from app.spot.stq.template import TemplateEngine
from app.spot.stq.stq import StqProductGenerator, StqApp, StqProduct


if TYPE_CHECKING:
    from app.resources import ResourceManager


class SpotStqRequestsHandler(SubscriptionNotificationHandler):
    @classmethod
    async def create(cls, resources:ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            requests_metadata_catalog_id = resources.config.spot.requests.metadata_catalog_id,
            stq_file_catalog_id=resources.config.spot.stq.file_catalog_id,
            stq_metadata_catalog_id=resources.config.spot.stq.metadata_catalog_id,
            subscription_id=resources.config.spot.requests.subscription_id,
            base_path=resources.config.spot.publisher.base_path,
            prefetch=resources.config.spot.requests.prefetch
        )
    
    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.someName.is_enabled

    def __init__(
        self,
        client: CatalogWebServiceClient,
        requests_metadata_catalog_id: str,
        stq_file_catalog_id: str, 
        stq_metadata_catalog_id: str,
        subscription_id: str,
        base_path:str,
        prefetch:Optional[int] = None
    ):
        super().__init__(client,subscription_id,prefetch=prefetch)
        self.__requests_metadata_catalog_id = requests_metadata_catalog_id
        self.__stq_file_catalog_id=stq_file_catalog_id
        self.__stq_metadata_catalog_id=stq_metadata_catalog_id
        self.__base_path = base_path

        self.__logger = logging.getLogger(__name__)

    async def _run(self, identity: CatalogIdentity, operation: Operation) -> None:
        new_request_record = await self.client.get_record(identity, coherence=DataCoherence.CONSISTENT)
        stq_file_catalog: CatalogAccessor = self.client.catalog(self.__stq_file_catalog_id)
        stq_metadata_catalog: CatalogAccessor = self.client.catalog(self.__stq_metadata_catalog_id)
        stq_file:CatalogIdentity = None
        request:StqApp = None
        stq:StqProduct = None

        try:
            # 1) Init Jinja template and Produce STQ object. 
            template_engine = TemplateEngine('./app/spot/stq/templates')
            data = [new_request_record.document]
            generator = StqProductGenerator(template_engine)
            
            request = StqApp(generator, data)
            request.run()
            
            stq = request.get_product()

            # 2) POST STQ product to the SPOT_STQ_FILE catalog
            file_record = CatalogRecord( file_metadata=CatalogRecordFileMetadata(content_type=MediaTypes.TEXT_PLAIN))
            file = CatalogFile(file_record,stq.body)

            stq_file = await stq_file_catalog.create_file(file) 

            # 3) POST data about STQ prodcut to SPOT_STQ_METADATA catalog and link with SPOT_STQ_FILE catalog
            metadata_stq_file_record = {
                "WFO":stq.site,
                "Spot-Id":stq.id,
                "Update-Number":stq.update,
                "Submition-Time":stq.submit_time,
                "STQ":{
                    "Record-Identifier":stq_file.record_id,
                    "File_Url":self._file_url(stq_file_catalog.catalog_url,stq_file.record_id)
                }
            }

            metadata_record = CatalogRecord(document=metadata_stq_file_record)
            metadata_record_id = await stq_metadata_catalog.create_record(metadata_record)
            
            # 4) Send the STQ file to the T.G.
            filename = self._file_name(stq)
            path = f'{self.__base_path}/{filename}'
            temp_path = f'{self.__base_path}/.{filename}'

            async with stq_file_catalog.get_file(stq_file.record_id, coherence=DataCoherence.CONSISTENT) as catalog_file:
                self.__logger.info(f'Publishing {stq_file.record_id} (from {stq_file}) to {path}')

                async with aiofiles.open(temp_path, 'wb') as output_file:
                    async for chunk in catalog_file.data:
                        await output_file.write(chunk)

            self.__logger.debug(f'Moving {temp_path} to {path}')
            await aiofiles.os.rename(temp_path, path)
            #published_time = pendulum.now('UTC')
            
        except:
            traceback.print_exc()
            self.__logger.warning("\nSTQ NOT CREATED")

    def _file_url(self,catalog_url,file_record_id) -> str:
        return catalog_url+"/files/"+file_record_id
    
    def _file_name(self, stq:StqProduct)->str:
        return f"{stq.site}_{stq.id}.stq"