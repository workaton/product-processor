from __future__ import annotations

import logging
from typing import Any, Mapping, Optional, TYPE_CHECKING

from ngitws.catalog import CatalogIdentity, CatalogRecord
from ngitws.collections import DotPathResolver
from ngitws.typing import JsonObject
from ngitws.web import CatalogWebServiceClient, DataCoherence

from .base import ExtractionHandler, Extractor, SubscriptionNotificationHandler

if TYPE_CHECKING:
    from app.resources import ResourceManager


class CapExtractionHandler(ExtractionHandler):

    @classmethod
    async def create(cls, resources: ResourceManager) -> SubscriptionNotificationHandler:
        return cls(
            client=await resources.catalog_client(),
            extractor=await resources.extractor('CAP'),
            file_link_id='xml',
            prefetch=resources.config.extractors.cap.prefetch,
            subscription_id=resources.config.extractors.cap.subscription_id
        )

    @classmethod
    def is_enabled(cls, resources: ResourceManager) -> bool:
        return resources.config.extractors.cap.is_enabled

    def __init__(
            self,
            client: CatalogWebServiceClient,
            extractor: Extractor,
            subscription_id: str,
            prefetch: Optional[int] = None,
            file_link_id: str = 'xml'
    ):
        super().__init__(client, extractor, subscription_id, file_link_id, prefetch)
        self.__logger = logging.getLogger(__name__)

    def _extract_extras(self, extracted_metadata: JsonObject) -> Mapping[str, Any]:
        resolver = DotPathResolver(extracted_metadata)
        return {
            'cap_id': resolver.get('alert.identifier'),
            'cap_category': resolver.get('alert.info.category'),
            'cap_event_name': resolver.get('alert.info.event'),
            'cap_certainty': resolver.get('alert.info.certainty'),
            'cap_severity': resolver.get('alert.info.severity'),
            'cap_urgency': resolver.get('alert.info.urgency'),
        }

    async def _update_catalog(
        self,
        identity: CatalogIdentity,
        metadata_record: CatalogRecord,
        extracted_metadata: JsonObject
    ) -> None:
        """Create an updated metadata record to replace the old one."""
        resolver = DotPathResolver(extracted_metadata)
        cap_id = resolver.get('alert.identifier')
        accessor = self.client.catalog(identity.catalog_id)

        # Check whether a product already updates this one
        for record in await accessor.query_records(
            f'Doc.alert.references.identifier=={cap_id}',
            coherence=DataCoherence.CONSISTENT,
            sort='Storage.Publish-Date ASC',
            limit=1
        ):
            extracted_metadata = {**extracted_metadata, **self.__create_reference_patch(record.document)}

        await super()._upsert_record(identity, metadata_record, extracted_metadata)

        references = resolver.get('alert.references', [])
        if references:
            ref_ids = [ref['identifier'] for ref in references]
            self.__logger.debug(
                f'Updating replacement times for {len(ref_ids)} referenced products: {", ".join(ref_ids)}'
            )

            fiql = f'Doc.alert.identifier=in=({",".join(ref_ids)})'
            patch = self.__create_reference_patch(extracted_metadata)
            patched_num = await accessor.merge_patch_by_query(fiql, patch)
            if len(ref_ids) != patched_num:
                self.__logger.warning(
                    f'Expected to patch {len(ref_ids)} referenced CAP records but patched {patched_num}'
                )

    def __create_reference_patch(self, document: JsonObject) -> JsonObject:
        resolver = DotPathResolver(document)

        return {
            'replacedAt': resolver.get('alert.sent'),
            'replacedBy': resolver.get('alert.identifier')
        }
