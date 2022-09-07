try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata
from collections.abc import Callable

version: Callable[[str], str] = metadata.version

__version__ = version("aio-clients")
