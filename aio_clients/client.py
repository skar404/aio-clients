import asyncio
import copy
from typing import Optional, Dict, Any, Union, Tuple, List

import aiohttp

from . import multipart
from .struct import Response, Options, Middleware

Q_PARAMS_TYPE = Optional[Union[
    Dict[str, Union[str, int]],
    List[Tuple[str, Union[str, int]]]
]]


class Http:
    def __init__(
            self, *,
            host='',
            headers=None,
            option: Options | None = None,
            middleware: Middleware | None = None
    ):
        loop = asyncio.get_event_loop()
        self.host = host
        self.base_option = option or Options()

        session_params = {}
        if self.base_option.trace_config:
            session_params['trace_configs'] = [
                self.base_option.trace_config
            ]

        if self.base_option.session_kwargs:
            session_params.update(self.base_option.session_kwargs)

        self.session = aiohttp.ClientSession(
            loop=loop,
            timeout=self.base_option.timeout,
            **session_params,  # type: ignore
        )

        self.headers = headers
        if headers is None:
            self.headers = {'Content-Type': 'application/json'}

        if self.base_option.user_agent:
            self.headers['user-agent'] = self.base_option.user_agent

        if middleware:
            self._middleware_start_list = middleware.start or []
            self._middleware_end_list = middleware.end or []
        else:
            self._middleware_start_list = []
            self._middleware_end_list = []

    async def middleware_start(
            self, *,
            headers: Dict[str, str] | None = None,
            request_kwargs: Dict[str, Any] | None = None,
            **kwargs
    ):
        for m in self._middleware_start_list:
            await m(
                headers=headers,
                request_kwargs=request_kwargs,
                **kwargs
            )

    async def middleware_end(
            self, *,
            response: Response,
            **kwargs
    ):
        for m in self._middleware_end_list:
            await m(
                response=response,
                **kwargs
            )

    async def request(  # noqa: C901
            self,
            *,
            method: str,
            path: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None,

            query_params: Q_PARAMS_TYPE = None,
            json: Optional[Any] = None,
            data: Optional[Any] = None,
            form: Optional[multipart.Easy] = None,

            option: Options | None = None,
    ) -> Response:
        if not option:
            option = self.base_option

        r = {}
        if json:
            r['json'] = json
        if data or form:
            r['data'] = data or form
        if query_params:
            r['params'] = query_params

        if option.timeout:
            r['timeout'] = option.timeout
        if option.is_ssl is not None:
            r['ssl'] = option.is_ssl
        if option.request_kwargs:
            r.update(option.request_kwargs)

        if path:
            url = '{}{}'.format(self.host, path)
        else:
            url = self.host

        main_headers = copy.deepcopy(self.headers)
        if headers:
            main_headers.update(headers)
        if data and 'Content-Type' in main_headers:
            del main_headers['Content-Type']

        if form:
            main_headers.update(form.headers)

        await self.middleware_start(
            headers=main_headers,
            request_kwargs=r
        )

        try:
            async with self.session.request(
                    method=method,
                    url=url,
                    headers=main_headers,
                    **r,
            ) as response:
                res = Response(
                    response=response,
                    code=response.status,
                    headers=response.headers,
                    option=option,
                    body=await response.read()
                )
                if option.is_json:
                    res.json = await response.json()

                await self.middleware_end(
                    response=res,
                )

                return res
        finally:
            if option.is_close_session:
                await self.close()

    async def get(self, path: str | None = None, *,
                  headers: Optional[Dict[str, str]] = None,
                  q_params: Q_PARAMS_TYPE = None,
                  o: Options | None = None) -> Response:
        return await self.request(method='GET', path=path, query_params=q_params, headers=headers, option=o)

    async def head(self, path: str | None = None, *,
                   headers: Optional[Dict[str, str]] = None,
                   q_params: Q_PARAMS_TYPE = None,
                   o: Options | None = None) -> Response:
        return await self.request(method='HEAD', path=path, query_params=q_params, headers=headers, option=o)

    async def options(self, path: str | None = None, *,
                      headers: Optional[Dict[str, str]] = None,
                      q_params: Q_PARAMS_TYPE = None,
                      o: Options | None = None) -> Response:
        return await self.request(method='OPTIONS', path=path, query_params=q_params, headers=headers, option=o)

    async def post(self, path: str | None = None, *,
                   q_params: Q_PARAMS_TYPE = None,
                   json: Optional[Any] = None,
                   data: Optional[Any] = None,
                   form: Optional[multipart.Easy] = None,

                   headers: Optional[Dict[str, str]] = None,
                   o: Options | None = None) -> Response:
        return await self.request(method='POST', path=path, query_params=q_params, json=json, form=form, data=data,
                                  headers=headers, option=o)

    async def put(self, path: str | None = None, *,
                  q_params: Q_PARAMS_TYPE = None,
                  json: Optional[Any] = None,
                  data: Optional[Any] = None,
                  form: Optional[multipart.Easy] = None,

                  headers: Optional[Dict[str, str]] = None,
                  o: Options | None = None) -> Response:
        return await self.request(method='PUT', path=path, query_params=q_params, json=json, form=form, data=data,
                                  headers=headers, option=o)

    async def patch(self, path: str | None = None, *,
                    q_params: Q_PARAMS_TYPE = None,
                    json: Optional[Any] = None,
                    data: Optional[Any] = None,
                    form: Optional[multipart.Easy] = None,

                    headers: Optional[Dict[str, str]] = None,
                    o: Options | None = None) -> Response:
        return await self.request(method='PATCH', path=path, query_params=q_params, json=json, form=form, data=data,
                                  headers=headers, option=o)

    async def delete(self, path: str | None = None, *,
                     q_params: Q_PARAMS_TYPE = None,
                     json: Optional[Any] = None,
                     data: Optional[Any] = None,
                     form: Optional[multipart.Easy] = None,

                     headers: Optional[Dict[str, str]] = None,
                     o: Options | None = None) -> Response:
        return await self.request(method='DELETE', path=path, query_params=q_params, json=json, form=form, data=data,
                                  headers=headers,
                                  option=o)

    async def trace(self, path: str | None = None, *,
                    q_params: Q_PARAMS_TYPE = None,
                    json: Optional[Any] = None,
                    data: Optional[Any] = None,
                    form: Optional[multipart.Easy] = None,
                    headers: Optional[Dict[str, str]] = None,
                    o: Options | None = None) -> Response:
        return await self.request(method='TRACE', path=path, query_params=q_params, json=json, form=form, data=data,
                                  headers=headers, option=o)

    async def close(self):
        await self.session.close()
