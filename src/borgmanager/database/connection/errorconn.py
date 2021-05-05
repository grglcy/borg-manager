from .databaseconnection import DatabaseConnection
from borgmanager.database.object import Error
from datetime import datetime


class ErrorConn(DatabaseConnection):
    def __init__(self, db_path, label_table: str, table_name: str = "errors"):
        self.label_table = label_table
        super().__init__(db_path, Error, table_name)

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"id INTEGER PRIMARY KEY," \
                           f"label_id INT NOT NULL," \
                           f"error TEXT NOT NULL," \
                           f"time TIMESTAMP NOT NULL," \
                           f"FOREIGN KEY (label_id) REFERENCES" \
                           f" {self.label_table} (id));"
        self.sql_execute(create_statement)

    def _exists(self, record, repo_id=None, archive_id=None, label_id=None):
        return None, None

    def _insert(self, record, repo_id=None, archive_id=None, label_id=None) -> int:
        if label_id is None:
            raise Exception("Label ID not supplied")
        with self.sql_lock:
            cursor = self.sql_cursor
            statement = f"INSERT INTO {self._sql_table}"\
                        f" ('label_id', 'error', 'time')"\
                        f" VALUES (?, ?, ?);"
            args = (label_id, record.error, datetime.now())
            cursor.execute(statement, args)
            self.sql_commit()
            return cursor.lastrowid
