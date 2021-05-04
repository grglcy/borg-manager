from datetime import datetime


class Error(object):
    def __init__(self, error: str, time: datetime):
        self.error = error
        self.time = time

    @classmethod
    def from_json(cls, json: dict):
        error = json['error']
        time = datetime.fromisoformat(json['time'])
        return cls(error, time)

    @classmethod
    def from_sql(cls, sql: list):
        pass
