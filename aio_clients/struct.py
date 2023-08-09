from dataclasses import dataclass
from typing import Any, Dict, List

from aiohttp import ClientTimeout, TraceConfig, ClientResponse
from multidict import CIMultiDictProxy

from .__version__ import __version__
from .types import MiddlewareStart, MiddlewareEnd


@dataclass
class Options:
    is_json: bool = True

    # off ssl validate
    is_ssl: bool | None = True

    # use only one reqeust
    is_close_session: bool = False

    timeout: ClientTimeout = ClientTimeout(10)
    trace_config: TraceConfig | None = None
    user_agent: str = f'aio-clients/{__version__}'

    session_kwargs: Dict[str, Any] | None = None
    request_kwargs: Dict[str, Any] | None = None


@dataclass
class Middleware:
    start: List[MiddlewareStart] | None = None
    end: List[MiddlewareEnd] | None = None


@dataclass
class Response:
    code: int

    headers: CIMultiDictProxy

    option: Options

    response: ClientResponse

    body: Any | None = None
    json: Any | None = None

    async def read_json(self) -> Any:
        self.json = await self.response.json()
        return self.json
