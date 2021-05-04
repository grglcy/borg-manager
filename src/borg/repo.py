from datetime import datetime
from pathlib import Path


class Repo(object):
    def __init__(self, fingerprint: str, location: Path, last_modified: datetime):
        self.fingerprint = fingerprint
        self.location = location
        self.last_modified = last_modified

    @classmethod
    def from_json(cls, json: dict):
        uuid = json['id']
        location = Path(json['location'])
        last_modified = datetime.fromisoformat(json['last_modified'])
        return cls(uuid, location, last_modified)

    @classmethod
    def from_sql(cls, sql: list):
        pass