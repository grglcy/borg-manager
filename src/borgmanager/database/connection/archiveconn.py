from .databaseconnection import DatabaseConnection
from datetime import datetime
from borgmanager.database.object import Archive


class ArchiveConn(DatabaseConnection):
    def __init__(self, db_path, repo_table: str,
                 table_name: str = "archive"):
        self.repo_table = repo_table
        super().__init__(db_path, table_name)

    # region INIT

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"id INTEGER PRIMARY KEY," \
                           f"fingerprint TEXT NOT NULL UNIQUE," \
                           f"repo_id INTEGER NOT NULL," \
                           f"name TEXT NOT NULL," \
                           f"start TEXT TIMESTAMP NULL," \
                           f"end TEXT TIMESTAMP NULL," \
                           f"file_count INTEGER NOT NULL," \
                           f"original_size INTEGER NOT NULL," \
                           f"compressed_size INTEGER NOT NULL," \
                           f"deduplicated_size INTEGER NOT NULL," \
                           f"FOREIGN KEY (repo_id) REFERENCES" \
                           f" {self.repo_table} (id));"
        self.sql_execute(create_statement)

    # endregion

    # region INSERT

    def _exists(self, record, repo_id=None, archive_id=None, label_id=None):
        return f"SELECT id FROM {self._sql_table}" \
               f" WHERE fingerprint=?;", (record.fingerprint,)

    def _insert(self, record, repo_id=None, archive_id=None, label_id=None) -> int:
        if repo_id is None:
            raise Exception("Repo id not supplied")
        with self.sql_lock:
            cursor = self.sql_cursor
            statement = f"INSERT INTO {self._sql_table}"\
                        f" ('fingerprint', 'repo_id', 'name', 'start', 'end'," \
                        f"'file_count', 'original_size', 'compressed_size', 'deduplicated_size')"\
                        f" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
            args = (record.fingerprint, repo_id, record.name,
                    record.start, record.end, record.file_count, record.original_size,
                    record.compressed_size, record.deduplicated_size)
            cursor.execute(statement, args)
            self.sql_commit()
            return cursor.lastrowid

    # endregion

    # region QUERIES

    def get_latest(self, repo_id: int):
        return self.sql_execute_one(f"SELECT * FROM {self._sql_table} WHERE repo_id = ?"
                                    f" ORDER BY id DESC LIMIT 1;", (repo_id,))

    def archive_on_hour(self, repo_id, date: datetime):
        date_string = str(date.date())
        hour_string = str(date.hour).zfill(2)
        result = self.sql_execute_all(f"SELECT * FROM {self._sql_table}"
                                      f" WHERE DATE(start) = DATE(?)"
                                      f" AND strftime('%H', start) = ?"
                                      f" AND repo_id = ?;",
                                      (date_string, hour_string, repo_id))
        return len(result) > 0

    def archive_on_date(self, repo_id, date: datetime):
        date_string = str(date.date())
        result = self.sql_execute_all(f"SELECT * FROM {self._sql_table}"
                                      f" WHERE DATE(start) = DATE(?)"
                                      f" AND repo_id = ?;",
                                      (date_string, repo_id))
        return len(result) > 0

    def between_dates(self, repo_id, first: datetime, last: datetime):
        first_string = str(first.date())
        last_string = str(last.date())
        result = self.sql_execute_all(f"SELECT * FROM {self._sql_table}"
                                      f" WHERE DATE(start) >= DATE(?)"
                                      f" AND DATE(start) <= DATE(?)"
                                      f" AND repo_id = ?",
                                      (first_string, last_string, repo_id))
        return len(result) > 0
    # endregion
