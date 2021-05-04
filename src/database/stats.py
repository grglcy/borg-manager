from . import DatabaseConnection, Repo, Archive


class Stats(DatabaseConnection):
    def __init__(self, db_path, repo: Repo, archive: Archive, stats_json: dict, table_name: str = "stats"):
        super().__init__(db_path, table_name)

        self.stat_id = None
        self.repo_id = repo.repo_id
        self.archive_id = archive.archive_id
        self.file_count = stats_json['nfiles']
        self.original_size = stats_json['original_size']
        self.compressed_size = stats_json['compressed_size']
        self.deduplicated_size = stats_json['deduplicated_size']

        self.stat_id = self._insert()

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"stat_id INTEGER PRIMARY KEY," \
                           f"repo_id INTEGER NOT NULL," \
                           f"archive_id INTEGER NOT NULL," \
                           f"file_count INTEGER NOT NULL UNIQUE," \
                           f"original_size INTEGER NOT NULL UNIQUE," \
                           f"compressed_size INTEGER NOT NULL UNIQUE," \
                           f"deduplicated_size INTEGER NOT NULL UNIQUE," \
                           f"FOREIGN KEY (repo_id) REFERENCES repo (repo_id)," \
                           f"FOREIGN KEY (archive_id) REFERENCES archive (archive_id))"
        self.sql_execute(create_statement)

    def _exists(self):
        return False

    def _insert(self) -> int:
        with self.sql_lock:
            cursor = self.sql_cursor
            statement = f"INSERT INTO {self._sql_table}"\
                        f" ('repo_id', 'archive_id', 'file_count', 'original_size'," \
                        f"'compressed_size', 'deduplicated_size')"\
                        f" VALUES (?, ?, ?, ?, ?, ?);"
            args = (self.repo_id, self.archive_id, self.file_count, self.original_size,
                    self.compressed_size, self.deduplicated_size)
            cursor.execute(statement, args)
            self.sql_commit()
            return cursor.lastrowid
