from typing import Dict, Type

from .fws.fws import FwsApp
from .stq.stq import StqApp

SPOT: Dict[str, any] = {
    "STQ": StqApp,
    "FWS": FwsApp
}

