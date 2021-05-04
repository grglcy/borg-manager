from datetime import datetime


class Archive(object):
    def __init__(self, fingerprint: str, name: str, start: datetime, end: datetime, primary_key=None):
        self.fingerprint = fingerprint
        self.name = name
        self.start = start
        self.end = end
        self.primary_key = primary_key

    @classmethod
    def from_json(cls, json: dict):
        uuid = json['id']
        name = json['name']
        start = datetime.fromisoformat(json['start'])
        end = datetime.fromisoformat(json['end'])
        return cls(uuid, name, start, end)

    @classmethod
    def from_sql(cls, sql: list):
        pass
