from dataclasses import dataclass
from typing import Any

from aiohttp import ClientTimeout


@dataclass
class Options:
    is_json: bool = True
    is_raw: bool = False
    timeout: ClientTimeout = None


@dataclass
class Response:
    status: int
    body: Any

    # FIXME: add type
    headers: Any

    option: Options
    raw_body: Any
