from .databaseconnection import DatabaseConnection


class LabelConn(DatabaseConnection):
    def __init__(self, db_path, repo_table: str,
                 table_name: str = "label"):
        self.repo_table = repo_table

        super().__init__(db_path, table_name)

    # region INIT

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"id INTEGER PRIMARY KEY," \
                           f"repo_id INT UNIQUE," \
                           f"label TEXT NOT NULL," \
                           f"FOREIGN KEY (repo_id) REFERENCES" \
                           f" {self.repo_table} (id));"
        self.sql_execute(create_statement)

    # endregion

    # region INSERT

    def _exists(self, record, repo_id=None, archive_id=None, label_id=None):
        if repo_id is None:
            return f"SELECT id FROM {self._sql_table} WHERE label=?;", (record.label,)
        else:
            return f"SELECT id FROM {self._sql_table} WHERE label=? OR repo_id=?;", (record.label, repo_id)

    def _insert(self, record, repo_id=None, archive_id=None, label_id=None) -> int:
        with self.sql_lock:
            cursor = self.sql_cursor
            if repo_id is None:
                statement = f"INSERT INTO {self._sql_table}"\
                            f" ('label')"\
                            f" VALUES (?);"
                args = (record.label,)
            else:
                statement = f"INSERT INTO {self._sql_table}" \
                            f" ('repo_id', 'label')" \
                            f" VALUES (?, ?);"
                args = (repo_id, record.label)
            cursor.execute(statement, args)
            self.sql_commit()
            return cursor.lastrowid

    def _update(self, record, primary_key, repo_id=None, archive_id=None, label_id=None):
        if repo_id is None:
            self.sql_execute(f"UPDATE {self._sql_table} SET label = ? WHERE id = ?;",
                             (record.label, primary_key))
        else:
            self.sql_execute(f"UPDATE {self._sql_table} SET repo_id = ?, label = ? WHERE id = ?;",
                             (repo_id, record.label, primary_key))
        self.sql_commit()

    # endregion

    # region QUERIES

    def get_repo_name(self, repo_id):
        result = self.sql_execute_one(f"SELECT label FROM {self._sql_table} WHERE repo_id = ?",
                                      (repo_id,))
        if result is None:
            return None
        else:
            return result[0]

    # endregion
