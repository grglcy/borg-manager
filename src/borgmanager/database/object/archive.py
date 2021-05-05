from . import DBObject
from datetime import datetime


class Archive(DBObject):
    def __init__(self, fingerprint: str, name: str, start: datetime, end: datetime, file_count: int, original_size: int,
                 compressed_size: int, deduplicated_size: int, primary_key=None):
        super(Archive, self).__init__(primary_key)
        self.fingerprint = fingerprint
        self.name = name
        self.start = start
        self.end = end
        self.file_count = file_count
        self.original_size = original_size
        self.compressed_size = compressed_size
        self.deduplicated_size = deduplicated_size

    @classmethod
    def from_json(cls, json: dict):
        fingerprint = json['id']
        name = json['name']
        start = datetime.fromisoformat(json['start'])
        end = datetime.fromisoformat(json['end'])

        stats_json = json['stats']
        file_count = stats_json['nfiles']
        original_size = stats_json['original_size']
        compressed_size = stats_json['compressed_size']
        deduplicated_size = stats_json['deduplicated_size']

        return cls(fingerprint, name, start, end, file_count, original_size, compressed_size, deduplicated_size)

    @classmethod
    def from_sql(cls, sql: list):
        pass
