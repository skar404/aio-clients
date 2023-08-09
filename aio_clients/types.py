import sys
from typing import Dict, Any, Awaitable, Optional, Union, Tuple, List

if sys.version_info > (3, 7):
    from typing import Protocol
else:
    Protocol = object


class MiddlewareStart(Protocol):
    def __call__(
            self,
            headers: Optional[Dict[str, str]] = None,
            request_kwargs: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Awaitable[None]: pass


class MiddlewareEnd(Protocol):
    def __call__(
            self,
            response,
            **kwargs
    ) -> Awaitable[None]: pass


Q_PARAMS_TYPE = Optional[Union[
    Dict[str, Union[str, int]],
    List[Tuple[str, Union[str, int]]]
]]
