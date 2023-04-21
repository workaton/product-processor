from __future__ import annotations

import asyncio
import logging
from typing import Dict, Optional

from ngitws.logging import track_correlation
from ngitws.monitoring import OperationResult, report_operation
from ngitws.web.client import CatalogAccessor


class ObsStationLocator:
    """Locator for obs stations for use in MDL encoders."""

    def __init__(self, accessor: CatalogAccessor):
        self.__accessor = accessor
        self.__population_lock = asyncio.Lock()
        self.__population_notifier = asyncio.Condition()
        self.__stations: Optional[Dict[str, str]] = None

        self.__logger = logging.getLogger(__name__)

    def get(self, station_id: str, default: str) -> Optional[str]:
        if self.__stations is None:
            raise RuntimeError('Tried to access obs station locator without populating data first')
        return self.__stations.get(station_id, default)

    async def populate_data(self) -> None:
        """Fetch and assemble obs station data."""
        if self.__population_lock.locked():
            # Just wait to finish if we're already pulling the data
            async with self.__population_lock:
                return

        with track_correlation():
            with report_operation('update_obs_station_geolocation_data') as operation:
                try:
                    async with self.__population_lock:
                        self.__logger.debug('Fetching obs station data')

                        stations: Dict[str, str] = {}
                        async with self.__accessor.query_records(properties=[
                            'Doc.id',
                            'Doc.name',
                            'Doc.elevationFeet',
                            'Doc.position'
                        ]) as records:
                            async for record in records:
                                station_id = record.document['id']
                                name = record.document['name']
                                lat = record.document['position']['coordinates'][1]
                                lon = record.document['position']['coordinates'][0]
                                elevation = float(record.document['elevationFeet']) / 0.3048
                                stations[station_id] = f'{name}||{lat:.3f} {lon:.3f} {elevation:.0f}'
                        self.__stations = stations
                        operation.message = f'Loaded geolocation data for {len(stations)} observation stations'
                except Exception as ex:
                    operation.ex = ex
                    operation.message = f'Failed to update geolocation data: {str(ex)}'
                    operation.result = OperationResult.FAIL

    async def wait_to_populate(self) -> None:
        if self.__stations is None:
            await self.populate_data()
