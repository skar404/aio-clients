import asyncio
from aio_clients import Http, Options


async def main():
    r = await Http().get('http://google.com', o=Options(is_json=False, is_raw=True, is_close_session=True))
    print(f'code={r.code} body={r.raw_body}')


asyncio.run(main())
