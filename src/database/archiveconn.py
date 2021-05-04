from . import DatabaseConnection


class ArchiveConn(DatabaseConnection):
    def __init__(self, db_path, table_name: str = "archive"):
        super().__init__(db_path, table_name)

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"archive_id INTEGER PRIMARY KEY," \
                           f"fingerprint INTEGER NOT NULL UNIQUE," \
                           f"repo_id INTEGER NOT NULL," \
                           f"name TEXT NOT NULL UNIQUE," \
                           f"start TEXT TIMESTAMP NULL," \
                           f"end TEXT TIMESTAMP NULL," \
                           f"FOREIGN KEY (repo_id) REFERENCES repo (repo_id))"
        self.sql_execute(create_statement)

    def _exists(self, record):
        return f"SELECT archive_id FROM {self._sql_table} WHERE fingerprint=?;", (record.fingerprint,)

    def _insert(self, record, repo_id) -> int:
        with self.sql_lock:
            cursor = self.sql_cursor
            statement = f"INSERT INTO {self._sql_table}"\
                        f" ('fingerprint', 'repo_id', 'name', 'start', 'end')"\
                        f" VALUES (?, ?, ?, ?, ?);"
            args = (record.fingerprint, repo_id, record.name, record.start, record.end)
            cursor.execute(statement, args)
            self.sql_commit()
            return cursor.lastrowid
