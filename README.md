# aiohttp client

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
    r = await Http().get('http://google.com', o=Options(is_json=False, is_raw=True, is_close_session=True))
    print(f'code={r.code} body={r.raw_body}')


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
        host='http://google.com/search?q=',
        trace_config=trace_config
    )

    r = await asyncio.gather(
        http.get('test', o=Options(is_json=False, is_raw=True)),
        http.get('hello world', o=Options(is_json=False, is_raw=True)),
        http.get('ping', o=Options(is_json=False, is_raw=True)),
    )

    print(f'status code={[i.code for i in r]}')
    await http.close()


asyncio.run(main())
```
