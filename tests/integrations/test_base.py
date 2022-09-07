import aiohttp
import pytest

from aio_clients.__version__ import __version__
from aio_clients import Http, Options
from aio_clients.multipart import Easy, Form, Writer

ECHO_HOST = 'localhost:8081'
ECHO_URL = f'http://{ECHO_HOST}/ping'


@pytest.mark.integtest
async def test_request():
    r = await Http(host=ECHO_URL, option=Options(is_json=False, is_close_session=True)).request(method='GET')

    assert r.code == 200
    assert r.body
    assert r.json is None

    r_json = await r.read_json()

    assert r.json
    assert r.json == r_json

    assert r_json['host']['hostname'] == 'localhost'
    assert r_json['http'] == {'method': 'GET', 'baseUrl': '', 'originalUrl': '/ping', 'protocol': 'http'}
    assert r_json['request'] == {
        'params': {'0': '/ping'}, 'query': {}, 'cookies': {}, 'body': {},
        'headers': {'host': ECHO_HOST, 'content-type': 'application/json',
                    'user-agent': f'aio-clients/{__version__}', 'accept': '*/*',
                    'accept-encoding': 'gzip, deflate'}
    }


@pytest.mark.integtest
async def test_request_json():
    r = await Http(host=ECHO_URL, option=Options(is_close_session=True)).request(method='GET')

    assert r.code == 200
    assert r.body
    assert r.json

    r_json = await r.read_json()

    assert r.json == r_json

    assert r_json['host']['hostname'] == 'localhost'
    assert r_json['http'] == {'method': 'GET', 'baseUrl': '', 'originalUrl': '/ping', 'protocol': 'http'}
    assert r_json['request'] == {
        'params': {'0': '/ping'}, 'query': {}, 'cookies': {}, 'body': {},
        'headers': {'host': ECHO_HOST, 'content-type': 'application/json',
                    'user-agent': f'aio-clients/{__version__}', 'accept': '*/*',
                    'accept-encoding': 'gzip, deflate'}
    }



@pytest.mark.integtest
async def test_request_multipart():
    http = Http(host=ECHO_URL, headers={'X-Token': '1234'})

    with Easy('form-data') as form:
        form.add_form(Form(key='chat_id', value=12345123))
        form.add_form(Form(key='audio', value='hello world'))

    writer = Writer()
    await form.write(writer)

    r = await http.request(
        method='POST',
        form=form,
    )

    assert r.code == 200
    assert r.json['host']['hostname'] == 'localhost'
    assert r.json['http'] == {'method': 'POST', 'baseUrl': '', 'originalUrl': '/ping', 'protocol': 'http'}
    assert r.json['request'] == {
        'params': {'0': '/ping'}, 'query': {}, 'cookies': {}, 'body': {'chat_id': '12345123', 'audio': 'hello world'},
        'headers': {'host': ECHO_HOST,
                    'content-type': f'multipart/form-data; boundary={form.boundary}',
                    'user-agent': f'aio-clients/{__version__}', 'x-token': '1234', 'accept': '*/*',
                    'accept-encoding': 'gzip, deflate',
                    'content-length': '352'}
    }

    raw_body = f"""--{form.boundary}\r
Content-Type: text/plain; charset=utf-8\r
Content-Length: 8\r
Content-Disposition: form-data; name="chat_id"\r
\r
12345123\r
--{form.boundary}\r
Content-Type: text/plain; charset=utf-8\r
Content-Length: 11\r
Content-Disposition: form-data; name="audio"\r
\r
hello world\r
--{form.boundary}--\r
"""
    assert writer.buffer.decode() == raw_body


@pytest.mark.integtest
async def test_request_case_001():
    http = Http(host=ECHO_URL, headers={'X-Token': '1234'})
    r = await http.request(
        method='POST',
        path='/upload',
        headers={'Supper-Header': 's1234'},
        json={'chat_id': 12345123, 'audio': 'hello world'},
    )
    assert r.code == 200
    assert r.body
    assert r.json['host']['hostname'] == 'localhost'
    assert r.json['http'] == {'method': 'POST', 'baseUrl': '', 'originalUrl': '/ping/upload', 'protocol': 'http'}
    assert r.json['request'] == {
        'params': {'0': '/ping/upload'}, 'query': {}, 'cookies': {},
        'body': {'chat_id': 12345123, 'audio': 'hello world'},
        'headers': {'host': ECHO_HOST, 'x-token': '1234',
                    'user-agent': f'aio-clients/{__version__}', 'supper-header': 's1234',
                    'accept': '*/*', 'accept-encoding': 'gzip, deflate',
                    'content-length': '45', 'content-type': 'application/json'}
    }


@pytest.mark.integtest
async def test_request_case_002():
    http = Http(host=ECHO_URL, headers={'X-Token': '1234'})
    r = await http.request(
        method='POST',
        path='/upload',
        headers={'Supper-Header': 's1234'},
        data={'chat_id': 12345123, 'audio': 'hello world'},
    )
    assert r.code == 200
    assert r.body
    assert r.json['host']['hostname'] == 'localhost'
    assert r.json['http'] == {'method': 'POST', 'baseUrl': '', 'originalUrl': '/ping/upload', 'protocol': 'http'}
    assert r.json['request'] == {
        'params': {'0': '/ping/upload'}, 'query': {}, 'cookies': {},
        'body': {'chat_id': '12345123', 'audio': 'hello world'},
        'headers': {'host': ECHO_HOST, 'x-token': '1234',
                    'user-agent': f'aio-clients/{__version__}', 'supper-header': 's1234',
                    'accept': '*/*', 'accept-encoding': 'gzip, deflate',
                    'content-length': '34', 'content-type': 'application/x-www-form-urlencoded'}
    }


@pytest.mark.integtest
async def test_request_not_save_method():
    http = Http(host=ECHO_URL, headers={'X-Token': '1234'})

    for request, method in (
            (http.post, 'POST'),
            (http.put, 'PUT'),
            (http.patch, 'PATCH'),
            (http.delete, 'DELETE'),
            (http.trace, 'TRACE'),
    ):
        r = await request(
            path='/upload',
            headers={'Supper-Header': 's1234'},
            data={'chat_id': 12345123, 'audio': 'hello world'},
        )

        assert r.code == 200
        assert r.body
        assert r.json['host']['hostname'] == 'localhost'
        assert r.json['http'] == {'method': method, 'baseUrl': '', 'originalUrl': '/ping/upload', 'protocol': 'http'}
        assert r.json['request'] == {
            'params': {'0': '/ping/upload'}, 'query': {}, 'cookies': {},
            'body': {'chat_id': '12345123', 'audio': 'hello world'},
            'headers': {'host': ECHO_HOST, 'x-token': '1234',
                        'user-agent': f'aio-clients/{__version__}', 'supper-header': 's1234',
                        'accept': '*/*', 'accept-encoding': 'gzip, deflate',
                        'content-length': '34', 'content-type': 'application/x-www-form-urlencoded'}
        }


@pytest.mark.integtest
async def test_request_save_method():
    http = Http(host=ECHO_URL, headers={'X-Token': '1234'})

    for request, method, body_empty in (
            (http.get, 'GET', False),
            (http.head, 'HEAD', True),
            (http.options, 'OPTIONS', False),
    ):
        r = await request(
            path='/upload',
            headers={'Supper-Header': 's1234'},
        )

        assert r.code == 200
        if body_empty:
            continue

        assert r.body
        assert r.json['host']['hostname'] == 'localhost'
        assert r.json['http'] == {'method': method, 'baseUrl': '', 'originalUrl': '/ping/upload', 'protocol': 'http'}
        assert r.json['request'] == {
            'params': {'0': '/ping/upload'}, 'query': {}, 'cookies': {}, 'body': {},
            'headers': {'host': ECHO_HOST, 'x-token': '1234', 'user-agent': f'aio-clients/{__version__}',
                        'supper-header': 's1234', 'accept': '*/*', 'accept-encoding': 'gzip, deflate'}
        }


@pytest.mark.integtest
async def test_request_trase_timeout():
    request = {
        'start': False,
        'end': False,
    }

    async def on_request_start(session, trace_config_ctx, params):
        request['start'] = True

    async def on_request_end(session, trace_config_ctx, params):
        request['end'] = True

    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)

    http = Http(
        host=ECHO_URL,
        option=Options(trace_config=trace_config),
    )
    r = await http.request(
        method='GET',
        option=Options(timeout=aiohttp.ClientTimeout(100)), path='/timeout'
    )

    assert r.code == 200
    assert r.body
    assert r.json

    assert request['start']
    assert request['end']


@pytest.mark.integtest
async def test_request_query_params():
    r = await Http(host=ECHO_URL, option=Options(is_close_session=True)) \
        .request(
        method='GET',
        query_params={
            'a': 1,
        })

    assert r.code == 200
    assert r.body
    assert r.json

    r_json = await r.read_json()

    assert r.json == r_json

    assert r_json['host']['hostname'] == 'localhost'
    assert r_json['http'] == {'method': 'GET', 'baseUrl': '', 'originalUrl': '/ping?a=1', 'protocol': 'http'}
    assert r_json['request'] == {
        'params': {'0': '/ping'}, 'query': {'a': '1'}, 'cookies': {}, 'body': {},
        'headers': {'host': ECHO_HOST, 'content-type': 'application/json',
                    'user-agent': f'aio-clients/{__version__}', 'accept': '*/*',
                    'accept-encoding': 'gzip, deflate'}
    }
