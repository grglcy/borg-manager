from . import DatabaseConnection, Repo
from datetime import datetime


class Archive(DatabaseConnection):
    def __init__(self, db_path, repo: Repo, archive_json: dict, table_name: str = "archive"):
        super().__init__(db_path, table_name)

        self.uuid = archive_json['id']
        self.repo_id = repo.repo_id
        self.name = archive_json['name']
        print(archive_json['start'])
        self.start = datetime.fromisoformat(archive_json['start'])
        self.end = datetime.fromisoformat(archive_json['end'])

        self.archive_id = self._insert()

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"archive_id INTEGER PRIMARY KEY," \
                           f"uuid INTEGER NOT NULL UNIQUE," \
                           f"repo_id INTEGER NOT NULL," \
                           f"name TEXT NOT NULL UNIQUE," \
                           f"start TEXT TIMESTAMP NULL," \
                           f"end TEXT TIMESTAMP NULL," \
                           f"FOREIGN KEY (repo_id) REFERENCES repo (repo_id))"
        self.sql_execute(create_statement)

    def _exists(self):
        result = self.sql_execute_one(f"SELECT archive_id FROM {self._sql_table}"
                                      f" WHERE uuid=?;", (self.uuid,))
        if result is None:
            return None
        else:
            return result[0]

    def _insert(self) -> int:
        if self._exists():
            raise Exception("archive with same uuid already exists")
        with self.sql_lock:
            cursor = self.sql_cursor
            statement = f"INSERT INTO {self._sql_table}"\
                        f" ('uuid', 'repo_id', 'name', 'start', 'end')"\
                        f" VALUES (?, ?, ?, ?, ?);"
            args = (self.uuid, self.repo_id, self.name, self.start, self.end)
            cursor.execute(statement, args)
            self.sql_commit()
            return cursor.lastrowid
