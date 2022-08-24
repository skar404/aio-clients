from dataclasses import dataclass
from typing import Any


@dataclass
class Form:
    key: str
    value: Any

    def get_value(self):
        if type(self.value) is int:
            return str(self.value)
        return self.value

    def params(self):
        return {}


@dataclass
class File(Form):
    file_name: str

    def params(self):
        return {
            'filename': self.file_name,
        }
