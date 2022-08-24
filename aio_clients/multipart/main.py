from aiohttp import MultipartWriter

from .struct import Form


class Easy(MultipartWriter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_form(self, form: Form):
        f = self.append(form.get_value())
        f.set_content_disposition(
            'form-data',
            name=form.key,
            **form.params()
        )
