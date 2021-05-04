from .databaseconnection import DatabaseConnection
from datetime import datetime


class ErrorConn(DatabaseConnection):
    def __init__(self, db_path, table_name: str = "errors"):
        super().__init__(db_path, table_name)

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"error_id INTEGER PRIMARY KEY," \
                           f"error TEXT NOT NULL," \
                           f"time TIMESTAMP NOT NULL);"
        self.sql_execute(create_statement)

    def _exists(self, record):
        return None, None

    def _insert(self, record, repo_id=None, archive_id=None) -> int:
        if repo_id is None or archive_id is None:
            raise Exception("Repo and archive ids not supplied")
        with self.sql_lock:
            cursor = self.sql_cursor
            statement = f"INSERT INTO {self._sql_table}"\
                        f" ('error', 'time')"\
                        f" VALUES (?, ?);"
            args = (record.error, datetime.now())
            cursor.execute(statement, args)
            self.sql_commit()
            return cursor.lastrowid
