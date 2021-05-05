from .databaseconnection import DatabaseConnection
from borgmanager.database.object import Cache


class CacheConn(DatabaseConnection):
    def __init__(self, db_path, archive_table: str, table_name: str = "cache"):
        self.archive_table = archive_table
        super().__init__(db_path, Cache, table_name)

    # region INIT

    def _create_table(self):
        create_statement = f"create table if not exists {self._sql_table}(" \
                           f"id INTEGER PRIMARY KEY," \
                           f"archive_id INT NOT NULL," \
                           f"total_chunks INT NOT NULL," \
                           f"total_csize INT NOT NULL," \
                           f"total_size INT NOT NULL," \
                           f"total_unique_chunks INT NOT NULL," \
                           f"unique_csize INT NOT NULL," \
                           f"unique_size INT NOT NULL," \
                           f"FOREIGN KEY (archive_id) REFERENCES" \
                           f" {self.archive_table} (id));"
        self.sql_execute(create_statement)

    # endregion

    # region INSERT

    def _exists(self, record, repo_id=None, archive_id=None, label_id=None):
        return None, None

    def _insert(self, record, repo_id=None, archive_id=None, label_id=None) -> int:
        if archive_id is None:
            raise Exception("Archive ID not supplied")
        else:
            with self.sql_lock:
                cursor = self.sql_cursor
                statement = f"INSERT INTO {self._sql_table}"\
                            f" ('archive_id', 'total_chunks', 'total_csize', 'total_size'," \
                            f"'total_unique_chunks', 'unique_csize', 'unique_size')"\
                            f" VALUES (?, ?, ?, ?, ?, ?, ?);"
                args = (archive_id, record.total_chunks, record.total_csize, record.total_size,
                        record.total_unique_chunks, record.unique_csize, record.unique_size)
                cursor.execute(statement, args)
                self.sql_commit()
                return cursor.lastrowid

    # endregion

    # region QUERIES

    def get(self, archive_id: int):
        return Cache.from_sql(self.sql_execute_one(f"SELECT * FROM {self._sql_table} WHERE archive_id = ?"
                                                   f" ORDER BY id DESC LIMIT 1;", (archive_id,)))

    # endregion
