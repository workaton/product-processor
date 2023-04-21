from __future__ import annotations

import multiprocessing
from pathlib import Path
from typing import Mapping, Optional

from cached_property import cached_property
from ngitws.cli import EnvironmentReader


DEFAULT_APP_NAME = 'product-processor'
DEFAULT_OBS_STATION_REFRESH = 120  # in seconds


class Configuration:

    def __init__(self, environ: Mapping[str, str]):
        self.__environ = environ
        self.__reader = EnvironmentReader(environ)

    @cached_property
    def app_name(self) -> str:
        return self.__reader.get('APP_NAME', DEFAULT_APP_NAME)

    @cached_property
    def catalog_password(self) -> str:
        return self.__reader.get('CATALOG_PASSWORD')

    @cached_property
    def catalog_url(self) -> str:
        return self.__reader.get('CATALOG_URL')

    @cached_property
    def catalog_username(self) -> str:
        return self.__reader.get('CATALOG_USERNAME')

    @cached_property
    def concurrency(self) -> int:
        return self.__reader.get_int('CONCURRENCY', multiprocessing.cpu_count())

    @cached_property
    def converters(self) -> ConvertersConfiguration:
        return ConvertersConfiguration(self.__reader)

    @cached_property
    def extractors(self) -> ExtractorsConfiguration:
        return ExtractorsConfiguration(self.__reader)

    @cached_property
    def spot(self)->SpotConfiguration:
        return SpotConfiguration(self.__reader) 

    @cached_property
    def graylog_web_url(self) -> str:
        return self.__reader.get('GRAYLOG_WEB_URL')

    @cached_property
    def ob_stations_catalog_id(self) -> str:
        return self.__reader.get('OB_STATIONS_CATALOG_ID')

    @cached_property
    def ob_stations_refresh(self) -> int:
        return self.__reader.get_int('OB_STATIONS_REFRESH', DEFAULT_OBS_STATION_REFRESH)

    @cached_property
    def socket_path(self) -> Path:
        return self.__reader.get_path('SOCKET_PATH', f'/run/{self.app_name}/{self.app_name}.sock')

    @cached_property
    def nwstg_publisher(self) -> NwstgPublisherConfiguration:
        return NwstgPublisherConfiguration(self.__reader, 'NWSTG_PUBLISHER')

    @cached_property
    def pubsub(self) -> PubsubConfiguration:
        return PubsubConfiguration(self.__reader)

    @cached_property
    def xymon_path(self) -> str:
        return self.__reader.get('XYMON_PATH')

    @cached_property
    def xymon_url(self) -> str:
        return self.__reader.get('XYMON_URL')


class ConvertersConfiguration:

    def __init__(self, reader: EnvironmentReader):
        self.airep = ConverterConfiguration(reader, 'AIREP_CONVERTER')
        self.csfpf = ConverterConfiguration(reader, 'CSFPF_CONVERTER')
        self.cwa = ConverterConfiguration(reader, 'CWA_CONVERTER')
        self.gfa = ConverterConfiguration(reader, 'GFA_CONVERTER')
        self.madis = ConverterConfiguration(reader, 'MADIS_CONVERTER')
        self.metar = ConverterConfiguration(reader, 'METAR_CONVERTER')
        self.mis = ConverterConfiguration(reader, 'MIS_CONVERTER')
        self.pirep = ConverterConfiguration(reader, 'PIREP_CONVERTER')
        self.sigmet = ConverterConfiguration(reader, 'SIGMET_CONVERTER')
        self.spc_watch = SpcWatchConverterConfiguration(reader, 'SPC_WATCH_CONVERTER')
        self.swb = ConverterConfiguration(reader, 'SWB_CONVERTER')
        self.taf = ConverterConfiguration(reader, 'TAF_CONVERTER')
        self.tca = ConverterConfiguration(reader, 'TCA_CONVERTER')
        self.tcf = ConverterConfiguration(reader, 'TCF_CONVERTER')
        self.vaa = ConverterConfiguration(reader, 'VAA_CONVERTER')
        self.wta = ConverterConfiguration(reader, 'WTA_CONVERTER')


class ExtractorsConfiguration:

    def __init__(self, reader: EnvironmentReader):
        self.airep = ExtractorConfiguration(reader, 'AIREP_EXTRACTOR')
        self.cap = ExtractorConfiguration(reader, 'CAP_EXTRACTOR')
        self.csfpf = ExtractorConfiguration(reader, 'CSFPF_EXTRACTOR')
        self.cwa = ExtractorConfiguration(reader, 'CWA_EXTRACTOR')
        self.mis = ExtractorConfiguration(reader, 'MIS_EXTRACTOR')
        self.pirep = ExtractorConfiguration(reader, 'PIREP_EXTRACTOR')
        self.saw = ExtractorConfiguration(reader, 'SAW_EXTRACTOR')
        self.sel = ExtractorConfiguration(reader, 'SEL_EXTRACTOR')
        self.sigmet = ExtractorConfiguration(reader, 'SIGMET_EXTRACTOR')
        self.swb = ExtractorConfiguration(reader, 'SWB_EXTRACTOR')
        self.tca = ExtractorConfiguration(reader, 'TCA_EXTRACTOR')
        self.tcf = ExtractorConfiguration(reader, 'TCF_EXTRACTOR')
        self.vaa = ExtractorConfiguration(reader, 'VAA_EXTRACTOR')
        self.wta = ExtractorConfiguration(reader, 'WTA_EXTRACTOR')

        self.madis = CollectiveExtractorConfiguration(reader, 'MADIS_EXTRACTOR')
        self.metar = CollectiveExtractorConfiguration(reader, 'METAR_EXTRACTOR')
        self.taf = CollectiveExtractorConfiguration(reader, 'TAF_EXTRACTOR')

class SpotConfiguration:
    def __init__(self,reader:EnvironmentReader):
        self.requests = SpotRequestsConfiguration(reader,'SPOT_REQUESTS')
        self.stq = SpotStqConfiguration(reader,'SPOT_STQ')
        self.publisher =SpotPublisherConfiguration(reader,'SPOT_PUBLISHER')
        self.fws = SpotFwsConfiguration(reader,'SPOT_FWS')


class PubsubConfiguration:

    def __init__(self, reader: EnvironmentReader):
        default_prefetch = reader.get_int('PREFETCH', 1)
        rmq_password = reader.get('RABBITMQ_PASSWORD')
        rmq_servers = reader.get_list('RABBITMQ_SERVERS')
        rmq_username = reader.get('RABBITMQ_USERNAME')
        rmq_vhost = reader.get('RABBITMQ_VHOST')

        self.amqp_urls = [f'amqp://{rmq_username}:{rmq_password}@{server}/{rmq_vhost}' for server in rmq_servers]
        self.prefetch = default_prefetch
        self.subws_url = reader.get('SUBWS_URL')
        self.subws_username = reader.get('SUBWS_USERNAME')
        self.subws_password = reader.get('SUBWS_PASSWORD')


class SubscriptionNotificationHandlerConfiguration:

    def __init__(self, reader: EnvironmentReader, name: str):
        self._env_prefix = name.upper()
        self._reader = reader

    @cached_property
    def is_enabled(self) -> bool:
        return self._reader.get_bool(f'{self._env_prefix}_ENABLE', True)

    @cached_property
    def prefetch(self) -> int:
        default_prefetch = self._reader.get_int('PREFETCH', 1)
        return self._reader.get_int(f'{self._env_prefix}_PREFETCH', default_prefetch)

    @cached_property
    def subscription_id(self) -> str:
        return self._reader.get(f'{self._env_prefix}_SUBSCRIPTION_ID')


class ConverterConfiguration(SubscriptionNotificationHandlerConfiguration):

    def __init__(self, reader: EnvironmentReader, name: str):
        super().__init__(reader, name)

    @cached_property
    def file_catalog_id(self) -> str:
        return self._reader.get(f'{self._env_prefix}_FILE_CATALOG_ID')


class ExtractorConfiguration(SubscriptionNotificationHandlerConfiguration):

    def __init__(self, reader: EnvironmentReader, name: str):
        super().__init__(reader, name)


class SpotRequestsConfiguration(SubscriptionNotificationHandlerConfiguration):
    def __init__(self, reader:EnvironmentReader, name:str):
        super().__init__(reader,name)
    
    @cached_property
    def metadata_catalog_id(self)->str:
        return self._reader.get(f'{self._env_prefix}_METADATA_CATALOG_ID')
    

class SpotPublisherConfiguration(SubscriptionNotificationHandlerConfiguration):
    def __init__(self,reader: EnvironmentReader, name:str):
        super().__init__(reader,name)
    
    @cached_property
    def base_path(self) -> str:
        return self._reader.get(f'{self._env_prefix}_BASE_PATH')


class SpotStqConfiguration(SubscriptionNotificationHandlerConfiguration):
    def __init__(self,reader: EnvironmentReader, name:str):
        super().__init__(reader,name)
    
    @cached_property
    def file_catalog_id(self)->str:
        return self._reader.get(f'{self._env_prefix}_FILE_CATALOG_ID')
    
    @cached_property
    def metadata_catalog_id(self)->str:
        return self._reader.get(f'{self._env_prefix}_METADATA_CATALOG_ID')

class SpotFwsConfiguration(SubscriptionNotificationHandlerConfiguration):
    def __init__(self,reader: EnvironmentReader, name:str):
        super().__init__(reader,name)

    @cached_property
    def file_catalog_id(self)->str:
        return self._reader.get(f'{self._env_prefix}_FILE_CATALOG_ID')
    
    @cached_property
    def metadata_catalog_id(self)->str:
        return self._reader.get(f'{self._env_prefix}_METADATA_CATALOG_ID')



class CollectiveExtractorConfiguration(SubscriptionNotificationHandlerConfiguration):

    def __init__(self, reader: EnvironmentReader, name: str):
        super().__init__(reader, name)

    @cached_property
    def file_catalog_id(self) -> Optional[str]:
        return self._reader.get(f'{self._env_prefix}_FILE_CATALOG_ID')

    @cached_property
    def metadata_catalog_id(self) -> str:
        return self._reader.get(f'{self._env_prefix}_METADATA_CATALOG_ID')


class NwstgPublisherConfiguration(SubscriptionNotificationHandlerConfiguration):

    def __init__(self, reader: EnvironmentReader, name: str):
        super().__init__(reader, name)

    @cached_property
    def base_path(self) -> str:
        return self._reader.get(f'{self._env_prefix}_BASE_PATH')

    @cached_property
    def catalog_id(self) -> str:
        return self._reader.get(f'{self._env_prefix}_CATALOG_ID')


class SpcWatchConverterConfiguration(SubscriptionNotificationHandlerConfiguration):

    def __init__(self, reader: EnvironmentReader, name: str):
        super().__init__(reader, name)

    @cached_property
    def saw_file_catalog_id(self) -> str:
        return self._reader.get(f'{self._env_prefix}_SAW_FILE_CATALOG_ID')

    @cached_property
    def saw_metadata_catalog_id(self) -> str:
        return self._reader.get(f'{self._env_prefix}_SAW_METADATA_CATALOG_ID')

    @cached_property
    def sel_file_catalog_id(self) -> str:
        return self._reader.get(f'{self._env_prefix}_SEL_FILE_CATALOG_ID')

    @cached_property
    def sel_metadata_catalog_id(self) -> str:
        return self._reader.get(f'{self._env_prefix}_SEL_METADATA_CATALOG_ID')
