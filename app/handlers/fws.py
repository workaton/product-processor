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
from app.spot.fws.fws import FwsApp, FwsParser, FwsProduct

if TYPE_CHECKING:
    from app.resources import ResourceManager


class SpotFwsHandler(SubscriptionNotificationHandler):
    
    @classmethod
    async def create(cls, resources:ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            fws_files_catalog_id = resources.config.spot.fws.file_catalog_id,
            fws_metadata_catalog_id=resources.config.spot.fws.metadata_catalog_id,
            stq_metadata_catalog_id=resources.config.spot.stq.metadata_catalog_id,
            subscription_id=resources.config.spot.requests.subscription_id,
            prefetch=resources.config.spot.requests.prefetch
        )
    
    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.converters.someName.is_enabled
    
    def __init__(
            self,
            client: CatalogWebServiceClient,
            fws_files_catalog_id: str,
            fws_metadata_catalog_id: str, 
            stq_metadata_catalog_id: str,
            subscription_id: str,
            prefetch:Optional[int] = None
    ):
        super().__init__(client,subscription_id,prefetch=prefetch)
        self.__fws_files_catalog_id = fws_files_catalog_id
        self.__fws_metadata_catalog_id =fws_metadata_catalog_id
        self.__stq_metadata_catalog_id =stq_metadata_catalog_id
        self.__logger = logging.getLogger(__name__)
    
    async def _run(self, identity: CatalogIdentity, operation: Operation) -> None:
        fws_catalog_accessor: CatalogAccessor = self.client.catalog(identity.catalog_id)
        # stq_metadata_catalog: CatalogAccessor = self.client.catalog(self.__stq_metadata_catalog_id)
        # fws_file:CatalogIdentity = None
        try:
            # 1. Get FWS product from the Catalog
            async with fws_catalog_accessor.get_file(identity.record_id, coherence=DataCoherence.CONSISTENT) as file:
                fws_raw_text = b''.join([d async for d in file.data])
                fws_text:str = fws_raw_text.decode("utf-8")
            
            # 2. Parse the FWS Product
            fws_parser = FwsParser()
            fws_app = FwsApp(fws_parser, fws_text)

            fws_app.run()
            product:FwsProduct = fws_app.get_product()

            # 3. Post metadata to NGITWS_FWS_METADATA catalog
            fws_metadata = {
                "Tag":product.id,
                "Spot_Id":product.id,
                "Forecaster":product.forecaster,
                "Update":product.update,
                "Corrected":product.corrected,
                "FWS":{
                    "Record-Identifier":identity.record_id,
                    "File_Url":self._file_url(fws_catalog_accessor.catalog_url, identity.record_id)
                }
            }

            fws_catalog_accessor = self.client.catalog(self.__fws_metadata_catalog_id)
            metadata_record = CatalogRecord(document=fws_metadata)
            metadata_record_id: CatalogIdentity  = await fws_catalog_accessor.create_record(metadata_record)

        except Exception:
            traceback.print_exc()

    def _file_url(self,catalog_url:str, file_record_id:str) -> str:
        return catalog_url+"/files/"+file_record_id

       