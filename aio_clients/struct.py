from dataclasses import dataclass
from typing import Any, Dict, Optional

from aiohttp import ClientTimeout
from multidict import CIMultiDictProxy


@dataclass
class Options:
    is_json: bool = True
    is_raw: bool = False

    # off ssl validate
    is_ssl: bool = True

    # use only one reqeust
    is_close_session: bool = False

    timeout: ClientTimeout = None


@dataclass
class Response:
    code: int

    headers: CIMultiDictProxy

    option: Options

    json: Optional[Dict[Any, Any]] = None
    raw_body: Optional[Any] = None
