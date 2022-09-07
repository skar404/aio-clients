import asyncio
from typing import Optional, Dict, Any, Union, Tuple, List

import aiohttp

from . import multipart
from .struct import Response, Options

Q_PARAMS_TYPE = Optional[Union[
    Dict[str, Union[str, int]],
    List[Tuple[str, Union[str, int]]]
]]


class Http:
    def __init__(
            self, *,
            host='',
            headers=None,
            option: Options = None,
    ):
        loop = asyncio.get_event_loop()
        self.host = host
        self.base_option = option or Options()

        session_params = {}
        if self.base_option.trace_config:
            session_params['trace_configs'] = [
                self.base_option.trace_config
            ]

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

            option: Options = None,
    ) -> Response:
        if not option:
            option = self.base_option

        r = {}
        if json:
            r['json'] = json
        if data:
            r['data'] = data
        if form:
            r['data'] = form
        if query_params:
            r['params'] = query_params

        if option.timeout:
            r['timeout'] = option.timeout

        if path:
            url = '{}{}'.format(self.host, path)
        else:
            url = self.host

        main_headers = self.headers.copy()
        if headers:
            main_headers.update(headers)

        if data and 'Content-Type' in main_headers:
            del main_headers['Content-Type']

        if form:
            main_headers.update(form.headers)

        async with self.session.request(
                method=method,
                url=url,
                headers=main_headers,
                ssl=option.is_ssl,
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
            if option.is_close_session:
                await self.close()

            return res

    async def get(self, path: str = None, *,
                  headers: Optional[Dict[str, str]] = None,
                  q_params: Q_PARAMS_TYPE = None,
                  o: Options = None) -> Response:
        return await self.request(method='GET', path=path, query_params=q_params, headers=headers, option=o)

    async def head(self, path: str = None, *,
                   headers: Optional[Dict[str, str]] = None,
                   q_params: Q_PARAMS_TYPE = None,
                   o: Options = None) -> Response:
        return await self.request(method='HEAD', path=path, query_params=q_params, headers=headers, option=o)

    async def options(self, path: str = None, *,
                      headers: Optional[Dict[str, str]] = None,
                      q_params: Q_PARAMS_TYPE = None,
                      o: Options = None) -> Response:
        return await self.request(method='OPTIONS', path=path, query_params=q_params, headers=headers, option=o)

    async def post(self, path: str = None, *,
                   q_params: Q_PARAMS_TYPE = None,
                   json: Optional[Any] = None,
                   data: Optional[Any] = None,
                   form: Optional[multipart.Easy] = None,

                   headers: Optional[Dict[str, str]] = None,
                   o: Options = None) -> Response:
        return await self.request(method='POST', path=path, query_params=q_params, json=json, form=form, data=data,
                                  headers=headers, option=o)

    async def put(self, path: str = None, *,
                  q_params: Q_PARAMS_TYPE = None,
                  json: Optional[Any] = None,
                  data: Optional[Any] = None,
                  form: Optional[multipart.Easy] = None,

                  headers: Optional[Dict[str, str]] = None,
                  o: Options = None) -> Response:
        return await self.request(method='PUT', path=path, query_params=q_params, json=json, form=form, data=data,
                                  headers=headers, option=o)

    async def patch(self, path: str = None, *,
                    q_params: Q_PARAMS_TYPE = None,
                    json: Optional[Any] = None,
                    data: Optional[Any] = None,
                    form: Optional[multipart.Easy] = None,

                    headers: Optional[Dict[str, str]] = None,
                    o: Options = None) -> Response:
        return await self.request(method='PATCH', path=path, query_params=q_params, json=json, form=form, data=data,
                                  headers=headers, option=o)

    async def delete(self, path: str = None, *,
                     q_params: Q_PARAMS_TYPE = None,
                     json: Optional[Any] = None,
                     data: Optional[Any] = None,
                     form: Optional[multipart.Easy] = None,

                     headers: Optional[Dict[str, str]] = None,
                     o: Options = None) -> Response:
        return await self.request(method='DELETE', path=path, query_params=q_params, json=json, form=form, data=data,
                                  headers=headers,
                                  option=o)

    async def trace(self, path: str = None, *,
                    q_params: Q_PARAMS_TYPE = None,
                    json: Optional[Any] = None,
                    data: Optional[Any] = None,
                    form: Optional[multipart.Easy] = None,

                    headers: Optional[Dict[str, str]] = None,
                    o: Options = None) -> Response:
        return await self.request(method='TRACE', path=path, query_params=q_params, json=json, form=form, data=data,
                                  headers=headers, option=o)

    async def close(self):
        await self.session.close()
