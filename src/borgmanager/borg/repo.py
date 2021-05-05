from . import DBObject
from datetime import datetime
from pathlib import Path


class Repo(DBObject):
    def __init__(self, fingerprint: str, location: Path, last_modified: datetime, primary_key=None):
        super(Repo, self).__init__(primary_key)
        self.fingerprint = fingerprint
        self.location = location
        self.last_modified = last_modified

    # region CLASS METHODS

    @classmethod
    def from_json(cls, json: dict):
        uuid = json['id']
        location = Path(json['location'])
        last_modified = datetime.fromisoformat(json['last_modified'])
        return cls(uuid, location, last_modified)

    @classmethod
    def from_sql(cls, sql: tuple):
        return cls(sql[1], sql[2], sql[3], sql[0])

    # endregion

    # region GET

    def seconds_since(self) -> float:
        return (datetime.now() - self.last_modified).total_seconds()

    # endregion
