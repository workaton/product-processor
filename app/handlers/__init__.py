# flake8: noqa F401
from typing import Dict, Type

from .base import CollectiveExtractionHandler, ConversionHandler, ExtractionHandler, SubscriptionNotificationHandler
from .airep import AirepConversionHandler, AirepExtractionHandler
from .cap import CapExtractionHandler
from .csfpf import CsfpfConversionHandler, CsfpfExtractionHandler
from .cwa import CwaConversionHandler, CwaExtractionHandler
from .gfa import GfaConversionHandler
from .madis import MadisCsvExtractionHandler, MadisJsonConversionHandler
from .metar import MetarCollectiveConversionHandler, MetarCollectiveExtractionHandler
from .mis import MisConversionHandler, MisExtractionHandler
from .nwstg import NwstgPublisherHandler
from .pirep import PirepConversionHandler, PirepExtractionHandler
from .sigmet import SigmetConversionHandler, SigmetExtractionHandler
from .spc import SpcWatchConversionHandler, SawExtractionHandler, SelExtractionHandler
from .swb import SwbConversionHandler, SwbExtractionHandler
from .taf import TafCollectiveConversionHandler, TafCollectiveExtractionHandler
from .tca import TcaConversionHandler, TcaExtractionHandler
from .tcf import TcfConversionHandler, TcfExtractionHandler
from .vaa import VolcanicAshConversionHandler, VolcanicAshExtractionHandler
from .wta import WtaConversionHandler, WtaExtractionHandler

from .stq import SpotStqRequestsHandler
from .fws import SpotFwsHandler


HANDLERS: Dict[str, Type[SubscriptionNotificationHandler]] = {
    'airep_converter': AirepConversionHandler,
    'airep_extractor': AirepExtractionHandler,
    'cap_extractor': CapExtractionHandler,
    'csfpf_converter': CsfpfConversionHandler,
    'csfpf_extractor': CsfpfExtractionHandler,
    'cwa_converter': CwaConversionHandler,
    'cwa_extractor': CwaExtractionHandler,
    'gfa_converter': GfaConversionHandler,
    'madis_csv_extractor': MadisCsvExtractionHandler,
    'madis_json_converter': MadisJsonConversionHandler,
    'metar_converter': MetarCollectiveConversionHandler,
    'metar_extractor': MetarCollectiveExtractionHandler,
    'mis_converter': MisConversionHandler,
    'mis_extractor': MisExtractionHandler,
    'nwstg_publisher': NwstgPublisherHandler,
    'pirep_converter': PirepConversionHandler,
    'pirep_extractor': PirepExtractionHandler,
    'sigmet_converter': SigmetConversionHandler,
    'sigmet_extractor': SigmetExtractionHandler,
    'saw_extractor': SawExtractionHandler,
    'sel_extractor': SelExtractionHandler,
    'spc_watch_converter': SpcWatchConversionHandler,
    'swb_converter': SwbConversionHandler,
    'swb_extractor': SwbExtractionHandler,
    'taf_converter': TafCollectiveConversionHandler,
    'taf_extractor': TafCollectiveExtractionHandler,
    'tca_converter': TcaConversionHandler,
    'tca_extractor': TcaExtractionHandler,
    'tcf_converter': TcfConversionHandler,
    'tcf_extractor': TcfExtractionHandler,
    'vaa_converter': VolcanicAshConversionHandler,
    'vaa_extractor': VolcanicAshExtractionHandler,
    'wta_converter': WtaConversionHandler,
    'wta_extractor': WtaExtractionHandler,
    'spot_stq_creator':SpotStqRequestsHandler,
    'spot_fws_handler': SpotFwsHandler,
}