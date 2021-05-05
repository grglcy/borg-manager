from . import DBObject
from datetime import datetime


class Error(DBObject):
    def __init__(self, error: str, time: datetime, primary_key=None):
        super(Error, self).__init__(primary_key)
        self.error = error.strip()
        self.time = time

    @classmethod
    def from_json(cls, json: dict):
        error = json['error']
        time = datetime.fromisoformat(json['time'])
        return cls(error, time)

    @classmethod
    def from_sql(cls, sql: list):
        pass
