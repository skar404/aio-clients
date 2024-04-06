from typing import Dict, Any, Optional, Union, Tuple, List

Q_PARAMS_TYPE = Optional[Union[
    Dict[str, Union[str, int]],
    List[Tuple[str, Union[str, int]]]
]]

# I don't know how to write this type
# for async function with kwargs
# FIXME maybe i fix this type later
# class MiddlewareStart(Protocol):
#     def __call__(
#             self,
#             headers: Optional[Dict[str, str]],
#             request_kwargs: Optional[Dict[str, Any]],
#             **kwargs: Any
#     ) -> Awaitable[None]: pass

MiddlewareStart = Any

# I don't know how to write this type
# for async function with kwargs
# FIXME maybe i fix this type later
# class MiddlewareEnd(Protocol):
#     def __call__(
#             self,
#             response,
#             **kwargs
#     ) -> Awaitable[None]: pass

MiddlewareEnd = Any
