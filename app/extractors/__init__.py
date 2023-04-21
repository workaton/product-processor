# flake8: noqa F401
from typing import Dict, Type

from .base import Extractor, IwxxmCollectiveExtractor, XmlExtractor
from .airep import AirepExtractor
from .cap import CapExtractor
from .csfpf import CsfpfExtractor
from .cwa import CwaExtractor
from .madis import MadisCsvExtractor
from .metar import MetarExtractor, MetarCollectiveExtractor
from .mis import MisExtractor
from .pirep import PirepExtractor
from .sigmet import SigmetExtractor
from .saw import SawExtractor
from .sel import SelExtractor
from .swb import SwbExtractor
from .taf import TafExtractor, TafCollectiveExtractor
from .tca import TcaExtractor
from .tcf import TcfExtractor
from .vaa import VolcanicAshExtractor
from .wta import WtaExtractor


EXTRACTORS: Dict[str, Type[Extractor]] = {
    'AIREP': AirepExtractor,
    'CAP': CapExtractor,
    'CSFPF': CsfpfExtractor,
    'CWA': CwaExtractor,
    'MADIS-CSV': MadisCsvExtractor,
    'METAR': MetarExtractor,
    'METAR-COLLECTIVE': MetarCollectiveExtractor,
    'MIS': MisExtractor,
    'PIREP': PirepExtractor,
    'SIGMET': SigmetExtractor,
    'SAW': SawExtractor,
    'SEL': SelExtractor,
    'SWB': SwbExtractor,
    'TAF': TafExtractor,
    'TAF-COLLECTIVE': TafCollectiveExtractor,
    'TCA': TcaExtractor,
    'TCF': TcfExtractor,
    'VAA': VolcanicAshExtractor,
    'WTA': WtaExtractor
}