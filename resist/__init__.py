__author__ = "Andy"
__license__ = "MIT"
__version__ = "0.1.0-alpha"

from typing import Literal, NamedTuple

from .client import *
from .rest import *
from .websocket import *


class Version(NamedTuple):
    major: int
    minor: int
    patch: int

    id: Literal["alpha", "beta", "final"]


version = Version(0, 1, 0, "alpha")
