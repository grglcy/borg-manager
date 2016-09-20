import sqlite3

class db_connection(object):
    
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
        if result.fetchone() == None:
            return False
        else:
            return True
