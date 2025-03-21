import json
import logging
from dataclasses import dataclass

from openpyxl.cell.cell import TYPE_ERROR


@dataclass
class Message:
    CODE_SUCCESS = 0
    CODE_FAILED = -1

    TYPE_ERROR = 'error'

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
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            logging.error('json parse error.', e)
            return cls(Message.CODE_FAILED, Message.TYPE_ERROR, 'json parse error.')

        return cls(data['code'], data['type'], data['detail'])

    def __str__(self):
        return f'Message{id(self)} code: {self.code}, type: {self.type}, detail: {self.detail}'