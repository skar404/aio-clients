from aio_clients.multipart import Easy, Form, File, Writer


async def test_form_data():
    with Easy('form-data') as form:
        form.add_form(Form(key='chat_id', value=12345123))
        form.add_form(Form(key='audio', value='hello world'))
        form.add_form(File(key='file', value=b'hello world file', file_name='test.py'))

    writer = Writer()
    await form.write(writer)

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
--{form.boundary}\r
Content-Type: application/octet-stream\r
Content-Length: 16\r
Content-Disposition: form-data; name="file"; filename="test.py"\r
\r
hello world file\r
--{form.boundary}--\r
"""

    assert dict(form.headers) == {'Content-Type': f'multipart/form-data; boundary={form.boundary}'}
    assert writer.buffer.decode() == raw_body
