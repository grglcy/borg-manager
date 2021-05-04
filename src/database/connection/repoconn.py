from .databaseconnection import DatabaseConnection


class RepoConn(DatabaseConnection):
    def __init__(self, db_path, table_name: str = 'repo'):
        super(RepoConn, self).__init__(db_path, table_name)

    def _insert(self, record, repo_id=None, archive_id=None) -> int:
        with self.sql_lock:
            cursor = self.sql_cursor
            statement = f"INSERT INTO {self._sql_table}"\
                        f" ('fingerprint', 'location', 'last_modified')"\
                        f" VALUES (?, ?, ?);"
            args = (record.fingerprint, str(record.location), record.last_modified)
            cursor.execute(statement, args)
            self.sql_commit()
            return cursor.lastrowid

    def _update(self, record, primary_key):
        self.sql_execute(f"UPDATE {self._sql_table} SET location = ?, last_modified = ? WHERE repo_id = ?;",
                         (str(record.location), record.last_modified, primary_key))
        self.sql_commit()

    def _exists(self, record):
        return f"SELECT repo_id FROM {self._sql_table} WHERE fingerprint=?;", (record.fingerprint,)

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"repo_id INTEGER PRIMARY KEY," \
                           f"fingerprint TEXT NOT NULL UNIQUE," \
                           f"location TEXT NOT NULL," \
                           f"last_modified TIMESTAMP NOT NULL)"
        self.sql_execute(create_statement)
