import asyncio

import pytest

from aio_clients import Http
from aio_clients.multipart import Easy, Form
from aio_clients.__version__ import __version__

ECHO_HOST = 'localhost:8081'
ECHO_URL = f'http://{ECHO_HOST}/'


@pytest.mark.integtest
async def test_async_case_001():
    http = Http(host=ECHO_URL)

    with Easy('form-data') as form:
        form.add_form(Form(key='chat_id', value=12345123))
        form.add_form(Form(key='audio', value='hello world'))

    with Easy('form-data') as form_new:
        form_new.add_form(Form(key='kino', value='1231jcsdin12nasd asdn12'))
        form_new.add_form(Form(key='sdg', value='sdaseqwe12'))

    r = await asyncio.gather(
        http.get('test', q_params=[('key', 'value1'), ('key', 'value2')], headers={'x-method': 'get reqeust'}),
        http.post('hello/world', json={'test': {'sd': 1233}}, headers={'x-method': 'post reqeust'}),
        http.post('ping', data={'1231214123123': 'asdads'}, headers={'x-method': 'delete reqeust'}),
        http.put('form/asd/12', form=form, headers={'x-method': 'put form reqeust'}),
        http.put('form/asdsasdad123/12?asdasd=1', form=form_new, headers={'x-method': 'put form reqeust'}),
    )

    assert len([True for i in r if i.code == 200]) == 5

    valid_data = [
        {
            'http': {'method': 'GET', 'baseUrl': '', 'originalUrl': '/test?key=value1&key=value2', 'protocol': 'http'},
            'request': {
                'params': {'0': '/test'}, 'query': {'key': ['value1', 'value2']}, 'cookies': {}, 'body': {},
                'headers': {'host': ECHO_HOST, 'content-type': 'application/json',
                            'user-agent': f'aio-clients/{__version__}', 'x-method': 'get reqeust', 'accept': '*/*',
                            'accept-encoding': 'gzip, deflate'}},
        },
        {
            'http': {'method': 'POST', 'baseUrl': '', 'originalUrl': '/hello/world', 'protocol': 'http'},
            'request': {
                'params': {'0': '/hello/world'}, 'query': {}, 'cookies': {}, 'body': {'test': {'sd': 1233}},
                'headers': {'host': ECHO_HOST, 'content-type': 'application/json',
                            'user-agent': f'aio-clients/{__version__}', 'x-method': 'post reqeust', 'accept': '*/*',
                            'accept-encoding': 'gzip, deflate', 'content-length': '22'}},
        },
        {
            'http': {'method': 'POST', 'baseUrl': '', 'originalUrl': '/ping', 'protocol': 'http'},
            'request': {
                'params': {'0': '/ping'}, 'query': {}, 'cookies': {}, 'body': {'1231214123123': 'asdads'},
                'headers': {'host': ECHO_HOST, 'user-agent': f'aio-clients/{__version__}',
                            'x-method': 'delete reqeust', 'accept': '*/*', 'accept-encoding': 'gzip, deflate',
                            'content-length': '20', 'content-type': 'application/x-www-form-urlencoded'}},
        },
        {
            'http': {'method': 'PUT', 'baseUrl': '', 'originalUrl': '/form/asd/12', 'protocol': 'http'},
            'request': {
                'params': {'0': '/form/asd/12'}, 'query': {}, 'cookies': {},
                'body': {'chat_id': '12345123', 'audio': 'hello world'},
                'headers': {'host': ECHO_HOST,
                            'content-type': f'multipart/form-data; boundary={form.boundary}',
                            'user-agent': f'aio-clients/{__version__}',
                            'x-method': 'put form reqeust',
                            'accept': '*/*',
                            'accept-encoding': 'gzip, deflate',
                            'content-length': '352'}},
        },
        {
            'http': {'method': 'PUT', 'baseUrl': '', 'originalUrl': '/form/asdsasdad123/12?asdasd=1',
                     'protocol': 'http'},
            'request': {'params': {'0': '/form/asdsasdad123/12'}, 'query': {'asdasd': '1'}, 'cookies': {},
                        'body': {'kino': '1231jcsdin12nasd asdn12', 'sdg': 'sdaseqwe12'},
                        'headers': {'host': ECHO_HOST,
                                    'content-type': f'multipart/form-data; boundary={form_new.boundary}',
                                    'user-agent': f'aio-clients/{__version__}', 'x-method': 'put form reqeust',
                                    'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'content-length': '362'}},
        },
    ]

    assert [{
        'http': i.json['http'],
        'request': i.json['request'],
    } for i in r] == valid_data

    await http.close()
