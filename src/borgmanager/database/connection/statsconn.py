from .databaseconnection import DatabaseConnection


class StatsConn(DatabaseConnection):
    def __init__(self, db_path, repo_table: str, archive_table: str,
                 table_name: str = "stats"):
        self.repo_table = repo_table
        self.archive_table = archive_table

        super().__init__(db_path, table_name)

    # region INIT

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"id INTEGER PRIMARY KEY," \
                           f"repo_id INTEGER NOT NULL," \
                           f"archive_id INTEGER NOT NULL," \
                           f"file_count INTEGER NOT NULL," \
                           f"original_size INTEGER NOT NULL," \
                           f"compressed_size INTEGER NOT NULL," \
                           f"deduplicated_size INTEGER NOT NULL," \
                           f"FOREIGN KEY (repo_id) REFERENCES" \
                           f" {self.repo_table} (id)," \
                           f"FOREIGN KEY (archive_id) REFERENCES" \
                           f" {self.archive_table} (id));"
        self.sql_execute(create_statement)

    # endregion

    # region INSERT

    def _exists(self, record, repo_id=None, archive_id=None, label_id=None):
        return None, None

    def _insert(self, record, repo_id=None, archive_id=None, label_id=None) -> int:
        if repo_id is None or archive_id is None:
            raise Exception("Repo and archive ids not supplied")
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

    # endregion

    # region QUERY

    def get_latest_stats(self, repo):
        key = repo.primary_key
        return self.sql_execute_one(f"SELECT * FROM {self._sql_table} WHERE repo_id=?;", (key,))

    # endregion
