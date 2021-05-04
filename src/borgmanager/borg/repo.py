from datetime import datetime
from pathlib import Path


class Repo(object):
    def __init__(self, fingerprint: str, location: Path, last_modified: datetime, primary_key=None):
        self.fingerprint = fingerprint
        self.location = location
        self.last_modified = last_modified
        self.__primary_key = primary_key

    @property
    def primary_key(self):
        if self.__primary_key is None:
            raise ValueError("Primary key is None")
        else:
            return self.__primary_key

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
