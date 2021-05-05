from . import DBObject


class Cache(DBObject):
    def __init__(self, total_chunks: int, total_csize: int, total_size: int, total_unique_chunks: int,
                 unique_csize: int, unique_size: int, primary_key=None):
        super(Cache, self).__init__(primary_key)
        self.total_chunks = total_chunks
        self.total_csize = total_csize
        self.total_size = total_size
        self.total_unique_chunks = total_unique_chunks
        self.unique_csize = unique_csize
        self.unique_size = unique_size

    @classmethod
    def from_json(cls, json: dict):
        total_chunks = json['total_chunks']
        total_csize = json['total_csize']
        total_size = json['total_size']
        total_unique_chunks = json['total_unique_chunks']
        unique_csize = json['unique_csize']
        unique_size = json['unique_size']
        return cls(total_chunks, total_csize, total_size, total_unique_chunks, unique_csize, unique_size)

    @classmethod
    def from_sql(cls, sql: tuple):
        primary_key = sql[0]
        total_chunks = sql[2]
        total_csize = sql[3]
        total_size = sql[4]
        total_unique_chunks = sql[5]
        unique_csize = sql[6]
        unique_size = sql[7]

        return cls(total_chunks, total_csize, total_size, total_unique_chunks,
                   unique_csize, unique_size, primary_key)
