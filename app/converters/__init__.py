# flake8: noqa F401
from typing import Dict, Type

from .base import ConversionInput, ConversionResult, Converter, ObsConverter
from .airep import AirepConverter
from .csfpf import CsfpfConverter
from .cwa import CwaConverter
from .gfa import GfaConverter
from .madis import MadisJsonConverter
from .metar import MetarCollectiveConverter
from .mis import MisConverter
from .pirep import PirepConverter
from .sigmet import SigmetConverter
from .spcwatch import SpcWatchConverter
from .swb import SwbConverter
from .taf import TafCollectiveConverter
from .tca import TcaConverter
from .tcf import TcfConverter
from .vaa import VolcanicAshConverter
from .wta import WtaConverter

CONVERTERS: Dict[str, Type[Converter]] = {
    'AIREP': AirepConverter,
    'CSFPF': CsfpfConverter,
    'CWA': CwaConverter,
    'GFA': GfaConverter,
    'MADIS-JSON': MadisJsonConverter,
    'METAR-COLLECTIVE': MetarCollectiveConverter,
    'MIS': MisConverter,
    'PIREP': PirepConverter,
    'SIGMET': SigmetConverter,
    'SPCWATCH': SpcWatchConverter,
    'SWB': SwbConverter,
    'TAF-COLLECTIVE': TafCollectiveConverter,
    'TCA': TcaConverter,
    'TCF': TcfConverter,
    'VAA': VolcanicAshConverter,
    'WTA': WtaConverter,
}
