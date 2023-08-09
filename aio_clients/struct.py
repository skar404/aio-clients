from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from aiohttp import ClientTimeout, TraceConfig, ClientResponse
from multidict import CIMultiDictProxy

from .__version__ import __version__
from .types import MiddlewareStart, MiddlewareEnd


@dataclass
class Options:
    is_json: bool = True

    # off ssl validate
    is_ssl: Optional[bool] = True

    # use only one reqeust
    is_close_session: bool = False

    timeout: ClientTimeout = ClientTimeout(10)
    trace_config: Optional[TraceConfig] = None
    user_agent: str = f'aio-clients/{__version__}'

    session_kwargs: Optional[Dict[str, Any]] = None
    request_kwargs: Optional[Dict[str, Any]] = None


@dataclass
class Middleware:
    start: Optional[List[MiddlewareStart]] = None
    end: Optional[List[MiddlewareEnd]] = None


@dataclass
class Response:
    code: int

    headers: CIMultiDictProxy

    option: Options

    response: ClientResponse

    body: Optional[Any] = None
    json: Optional[Any] = None

    async def read_json(self) -> Any:
        self.json = await self.response.json()
        return self.json
