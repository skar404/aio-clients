from importlib import metadata
from collections.abc import Callable

version: Callable[[str], str] = metadata.version

__version__ = version("aio-clients")
