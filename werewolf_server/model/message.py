import json
from dataclasses import dataclass


@dataclass
class Message:
    CODE_SUCCESS = 0
    CODE_FAILED = -1

    code: int
    type: str
    detail: str

    def __init__(self, code, type, detail):
        self.code = code
        self.type = type
        self.detail = detail

    def to_json(self):
        return json.dumps({
            'code': self.code,
            'type': self.type,
            'detail': self.detail
        }, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data['code'], data['type'], data['detail'])

    def __str__(self):
        return f'Message{id(self)} code: {self.code}, type: {self.type}, detail: {self.detail}'