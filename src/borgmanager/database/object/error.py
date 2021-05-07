from . import DBObject
from datetime import datetime, timezone


class Error(DBObject):
    def __init__(self, error: str, time: datetime, primary_key=None):
        super(Error, self).__init__(primary_key)
        self.error = error.strip()
        if not self.error:
            self.error = "No error information supplied"
        self.time = time

    @classmethod
    def from_json(cls, json: dict):
        error = json['error']
        time = datetime.fromisoformat(json['time']).astimezone(tz=timezone.utc).replace(tzinfo=None)
        return cls(error, time)

    @classmethod
    def from_sql(cls, sql: list):
        primary_key = sql[0]
        error = sql[2]
        time = sql[3]
        return cls(error, time, primary_key)
