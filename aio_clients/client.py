import asyncio
from typing import Optional, Dict, Any

import aiohttp
from aiohttp import TraceConfig

from .struct import Response, Options


class Writer:
    def __init__(self):
        self.buffer = bytearray()

    async def write(self, data):
        self.buffer.extend(data)


class Http:
    def __init__(
            self, *,
            host='',
            timeout=10,
            headers=None,
            trace_config: TraceConfig = None,
    ):
        loop = asyncio.get_event_loop()
        self.host = host
        self.timeout = aiohttp.ClientTimeout(
            total=timeout,
        )

        session_params = {}
        if trace_config:
            session_params['trace_configs'] = [
                trace_config,
            ]

        self.session = aiohttp.ClientSession(
            loop=loop,
            timeout=self.timeout,
            **session_params,
        )

        self.headers = headers
        if headers is None:
            self.headers = {
                'Content-Type': 'application/json',
                'user-agent': 'aio-clients/0.1.0b3'
            }

    async def request(
            self,
            *,
            method: str,
            path,
            headers: Optional[Dict[str, str]] = None,
            json: Optional[Any] = None,
            data=None,
            option: Options = None,
    ) -> Response:
        r = {}
        if json:
            r['json'] = json
        if data:
            r['data'] = data
        if not option:
            option = Options()

        if option.timeout:
            r['timeout'] = option.timeout

        url = '{}{}'.format(self.host, path)

        main_headers = self.headers.copy()
        if headers:
            main_headers.update(headers)

        async with self.session.request(
                method=method,
                url=url,
                headers=main_headers,
                ssl=option.is_ssl,
                **r,
        ) as response:
            r = Response(
                code=response.status,
                headers=response.headers,
                option=option,
            )

            if option.is_json:
                r.json = await response.json()
            if option.is_raw:
                r.raw_body = await response.read()
            if option.is_close_session:
                await self.close()

            return r

    async def get(self, path, *, headers: Optional = None, o: Options = None):
        return await self.request(method='GET', path=path, headers=headers, option=o)

    async def head(self, path, *, headers: Optional = None, o: Options = None):
        return await self.request(method='HEAD', path=path, headers=headers, option=o)

    async def post(self, path, *, data=None, headers: Optional = None, json: Optional = None, o: Options = None):
        return await self.request(method='POST', path=path, headers=headers, json=json, data=data, option=o)

    async def put(self, path, *, data=None, headers: Optional = None, json: Optional = None, o: Options = None):
        return await self.request(method='PUT', path=path, headers=headers, json=json, data=data, option=o)

    async def delete(self, path, *, data=None, headers: Optional = None, json: Optional = None, o: Options = None):
        return await self.request(method='DELETE', path=path, headers=headers, json=json, data=data, option=o)

    async def connect(self, path, *, data=None, headers: Optional = None, json: Optional = None, o: Options = None):
        return await self.request(method='CONNECT', path=path, headers=headers, json=json, data=data, option=o)

    async def options(self, path, *, data=None, headers: Optional = None, json: Optional = None, o: Options = None):
        return await self.request(method='OPTIONS', path=path, headers=headers, json=json, data=data, option=o)

    async def trace(self, path, *, data=None, headers: Optional = None, json: Optional = None, o: Options = None):
        return await self.request(method='TRACE', path=path, headers=headers, json=json, data=data, option=o)

    async def patch(self, path, *, data=None, headers: Optional = None, json: Optional = None, o: Options = None):
        return await self.request(method='PATCH', path=path, headers=headers, json=json, data=data, option=o)

    async def close(self):
        await self.session.close()
