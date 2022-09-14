# aiohttp client

[![Tests](https://github.com/skar404/aio-clients/actions/workflows/python-tests.yml/badge.svg)](https://github.com/skar404/aio-clients/actions/workflows/python-tests.yml)
[![Published](https://github.com/skar404/aio-clients/actions/workflows/python-publish.yml/badge.svg)](https://github.com/skar404/aio-clients/actions/workflows/python-publish.yml)
[![Coverage Status](https://coveralls.io/repos/github/skar404/aio-clients/badge.svg?branch=master)](https://coveralls.io/github/skar404/aio-clients?branch=master)
[![PyPi version](https://badgen.net/pypi/v/aio-clients/)](https://pypi.org/project/aio-clients)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aio-clients)](https://pypi.org/project/aio-clients)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/aio-clients)](https://pypi.org/project/aio-clients)
[![PyPI - License](https://img.shields.io/pypi/l/aio-clients)](https://pypi.org/project/aio-clients)

### What is the difference from aiohttp.Client?

It is simpler and as a Requests

----

## Install beta:

```bash
pip install aio-clients
```

----

# Example:

## Base reqeust:

```python
import asyncio
from aio_clients import Http, Options


async def main():
    r = await Http().get('https://google.com', o=Options(is_json=False, is_close_session=True))
    print(f'code={r.code} body={r.body}')


asyncio.run(main())
```

## Async reqeust

```python
import asyncio

import aiohttp
from aio_clients import Http, Options


async def on_request_start(session, trace_config_ctx, params):
    print("Starting request")


async def on_request_end(session, trace_config_ctx, params):
    print("Ending request")


async def main():
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)

    http = Http(
        host='https://google.com/search',
        option=Options(trace_config=trace_config, is_json=False),
    )

    r = await asyncio.gather(
        http.get(q_params={'q': 'test'}),
        http.get(q_params={'q': 'hello_world'}),
        http.get(q_params={'q': 'ping'}),
    )

    print(f'status code={[i.code for i in r]} body={[i.body for i in r]}')
    await http.close()


asyncio.run(main())
```

## Multipart reqeust:

```python
import asyncio
from aio_clients import Http, Options
from aio_clients.multipart import Easy, Form, File, Writer


async def main():
    with Easy('form-data') as form:
        form.add_form(Form(key='chat_id', value=12345123))
        form.add_form(Form(key='audio', value='hello world'))
        form.add_form(File(key='file', value=b'hello world file', file_name='test.py'))

    r = await Http(option=Options(is_close_session=True, is_json=False)).post(
        'http://localhost:8081',
        form=form,
    )

    writer = Writer()
    await form.write(writer)

    print(f'code={r.code} body={r.body}')
    print(f'full body:\n{writer.buffer.decode()}')


asyncio.run(main())
```


