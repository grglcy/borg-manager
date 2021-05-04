from abc import ABC, abstractmethod
from threading import Lock
import sqlite3


class DatabaseConnection(ABC):
    def __init__(self, db_path, table_name: str):
        self.__sql_lock = Lock()

        self.__sql_database = sqlite3.connect(db_path,
                                              detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                                              check_same_thread=False)

        self._sql_table = table_name

        self._create_table()
        self.sql_commit()

    # region INIT

    @abstractmethod
    def _create_table(self):
        raise NotImplementedError

    # endregion

    # region PROPERTIES

    @property
    def sql_lock(self):
        return self.__sql_lock

    @property
    def sql_cursor(self):
        return self.__sql_database.cursor()

    # endregion

    # region GENERIC SQL

    def sql_commit(self):
        self.__sql_database.commit()

    def sql_execute(self, statement: str, args: tuple = None):
        with self.__sql_lock:
            cursor = self.sql_cursor
            if args is None:
                cursor.execute(statement)
            else:
                cursor.execute(statement, args)

    def sql_execute_row_id(self, statement: str, args: tuple = None):
        with self.__sql_lock:
            cursor = self.sql_cursor
            if args is None:
                cursor.execute(statement)
            else:
                cursor.execute(statement, args)
            cursor.execute(f"select last_insert_rowid() from {self._sql_table};")
            row_id = cursor.fetchone()
            return row_id[0]

    def sql_execute_all(self, statement: str, args: tuple = None):
        with self.__sql_lock:
            cursor = self.sql_cursor
            if args is None:
                cursor.execute(statement)
            else:
                cursor.execute(statement, args)

            return cursor.fetchall()

    def sql_execute_one(self, statement: str, args: tuple = None):
        with self.__sql_lock:
            cursor = self.sql_cursor
            if args is None:
                cursor.execute(statement)
            else:
                cursor.execute(statement, args)

            return cursor.fetchone()

    # endregion

    # region MODIFICATION

    def insert(self, record, repo_id=None, archive_id=None):
        exists, primary_key = self.exists(record)
        if exists:
            self._update(record, primary_key)
            return primary_key
        else:
            return self._insert(record, repo_id, archive_id)

    def _update(self, record, primary_key):
        pass

    @abstractmethod
    def _insert(self, record, repo_id=None, archive_id=None) -> int:
        raise NotImplementedError

    def exists(self, record) -> (bool, int):
        query, args = self._exists(record)

        if query is None:
            return False, None
        else:
            result = self.sql_execute_one(query, args)
            if result is None:
                return False, None
            else:
                return True, result[0]

    @abstractmethod
    def _exists(self, record) -> (str, tuple):
        raise NotImplementedError

    # endregion

    # region QUERIES

    def get_all(self):
        result = self.sql_execute_one(f"SELECT * FROM {self._sql_table};")
        if result is None:
            return None
        else:
            return result[0]

    # endregion

    def stop(self):
        with self.__sql_lock:
            self.sql_commit()
            self.__sql_database.close()

