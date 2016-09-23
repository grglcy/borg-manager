import sqlite3


class Database(object):
    
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
    
    def __del__(self):
        self.conn.close()
    
    def create_table(self, name, row_list):
        """creates table 'name' with rows from 'row_list' if it doesn't exist"""

        if self.table_exists(name):
            return True
        
        else:
            rows = ""
            separator = ", "
            for i in range(0, len(row_list)):
                if i == len(row_list) - 1:
                    separator = ""
                rows += "%s%s" % (row_list[i], separator)
            
            self.conn.execute("CREATE TABLE %s(%s)" % (name, rows))
            if self.table_exists(name):
                return True
            else:
                return False
    
    def table_exists(self, name):
        """returns true if table 'name' exists"""

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
                                        log_entry.duration,
                                        log_entry.file_count))
            self.conn.commit()

    def query(self, query):
        return self.conn.execute(query).fetchall()

    def query_year(self, table, year):
        return self.query("""SELECT * FROM %s WHERE strftime(\"%%Y\",
                          START_TIME) == \"%s\"""" % (table, year))
