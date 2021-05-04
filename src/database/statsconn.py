from . import DatabaseConnection


class StatsConn(DatabaseConnection):
    def __init__(self, db_path, table_name: str = "stats"):
        super().__init__(db_path, table_name)

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"stat_id INTEGER PRIMARY KEY," \
                           f"repo_id INTEGER NOT NULL," \
                           f"archive_id INTEGER NOT NULL," \
                           f"file_count INTEGER NOT NULL," \
                           f"original_size INTEGER NOT NULL," \
                           f"compressed_size INTEGER NOT NULL," \
                           f"deduplicated_size INTEGER NOT NULL," \
                           f"FOREIGN KEY (repo_id) REFERENCES repo (repo_id)," \
                           f"FOREIGN KEY (archive_id) REFERENCES archive (archive_id))"
        self.sql_execute(create_statement)

    def _exists(self, record):
        return None, None

    def _insert(self, record, repo_id, archive_id) -> int:
        with self.sql_lock:
            cursor = self.sql_cursor
            statement = f"INSERT INTO {self._sql_table}"\
                        f" ('repo_id', 'archive_id', 'file_count', 'original_size'," \
                        f"'compressed_size', 'deduplicated_size')"\
                        f" VALUES (?, ?, ?, ?, ?, ?);"
            args = (repo_id, archive_id, record.file_count, record.original_size,
                    record.compressed_size, record.deduplicated_size)
            cursor.execute(statement, args)
            self.sql_commit()
            return cursor.lastrowid
