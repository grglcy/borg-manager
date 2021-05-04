from . import DatabaseConnection
from datetime import datetime


class Repo(DatabaseConnection):
    def __init__(self, db_path, repo_json: dict, table_name: str = 'repo'):
        super(Repo, self).__init__(db_path, table_name)

        self.uuid = repo_json['id']
        self.location = repo_json['location']
        self.last_modified = datetime.fromisoformat(repo_json['last_modified'])

        if self.exists():
            self._update()
        else:
            self.insert()

    def _insert(self) -> int:
        with self.sql_lock:
            cursor = self.sql_cursor
            statement = f"INSERT INTO {self._sql_table}"\
                        f" ('uuid', 'location', 'last_modified')"\
                        f" VALUES (?, ?, ?);"
            args = (self.uuid, self.location, self.last_modified)
            cursor.execute(statement, args)
            self.sql_commit()
            return cursor.lastrowid

    def _update(self):
        self.sql_execute(f"UPDATE {self._sql_table} SET location = ?, last_modified = ? WHERE repo_id = ?;",
                         (self.location, self.last_modified, self.primary_key))
        self.sql_commit()

    def _exists(self):
        result = self.sql_execute_one(f"SELECT repo_id FROM {self._sql_table}"
                                      f" WHERE uuid=?;", (self.uuid,))
        if result is None:
            return False, None
        else:
            return True, result[0]

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"repo_id INTEGER PRIMARY KEY," \
                           f"uuid INTEGER NOT NULL UNIQUE," \
                           f"location TEXT NOT NULL," \
                           f"last_modified TIMESTAMP NOT NULL)"
        self.sql_execute(create_statement)
