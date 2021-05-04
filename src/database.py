from logentry import LogEntry
import sqlite3


class Database(object):
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.table_name = "log"
        self.create_log_table()
    
    def __del__(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def create_log_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                    logID integer PRIMARY KEY,
                    name text NOT NULL,
                    fingerprint text NOT NULL,
                    start text NOT NULL,
                    end text NOT NULL,
                    filecount long NOT NULL);"""
        self.conn.execute(query)
        self.commit()

    def insert(self, log_entry: LogEntry):
        query = f"INSERT INTO {self.table_name} (name, fingerprint, start, end, filecount) VALUES(?,?,?,?,?)"
        self.conn.execute(query, (log_entry.name, log_entry.fingerprint, log_entry.start_time, log_entry.end_time,
                                  log_entry.file_count))
        self.commit()
