import sqlite3


class Database(object):
    
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
    
    def __del__(self):
        self.conn.close()
    
    def create_table(self, name, row_list):
        if self.table_exists(name):
            return True
        
        else:
            row_string = ""
            separator = ", "
            for i in range(0, len(row_list)):
                if i == len(row_list) - 1:
                    separator = ""
                row_string += "%s%s" % (row_list[i], separator)
            
            self.conn.execute("CREATE TABLE %s(%s)" % (name, row_string))
            if self.table_exists(name):
                return True
            else:
                return False
    
    def table_exists(self, name):
        result = self.conn.execute("""SELECT * FROM sqlite_master
                    WHERE type='table' AND name=?""", (name,))
        if result.fetchone() is None:
            return False
        else:
            return True

    def insert(self, log_entry, table):
            result = self.conn.execute("""INSERT INTO %s(NAME,
            FINGERPRINT, START_TIME, DURATION, FILE_COUNT) VALUES(?,?,?,?,?)"""
                                       % table,
                                       (log_entry.name,
                                        log_entry.fingerprint,
                                        log_entry.datetime_string(),
                                        "1",
                                        log_entry.file_count))
            self.conn.commit()
