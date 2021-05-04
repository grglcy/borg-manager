class Stats(object):
    def __init__(self, file_count: int, original_size: int, compressed_size: int, deduplicated_size: int,
                 primary_key=None):
        self.file_count = file_count
        self.original_size = original_size
        self.compressed_size = compressed_size
        self.deduplicated_size = deduplicated_size
        self.__primary_key = primary_key

    @property
    def primary_key(self):
        if self.__primary_key is None:
            raise ValueError("Primary key is None")
        else:
            return self.__primary_key

    @classmethod
    def from_json(cls, json: dict):
        file_count = json['nfiles']
        original_size = json['original_size']
        compressed_size = json['compressed_size']
        deduplicated_size = json['deduplicated_size']
        return cls(file_count, original_size, compressed_size, deduplicated_size)

    @classmethod
    def from_sql(cls, sql: tuple):
        key = sql[0]
        filecount = sql[3]
        original_size = sql[4]
        compressed_size = sql[5]
        deduplicated_size = sql[6]
        return cls(filecount, original_size, compressed_size, deduplicated_size, key)
