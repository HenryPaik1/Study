import pymysql
import ch6_dbconfig

class DBHelper:
    
    def connect(self, database="crimemap"):
        return pymysql.connect(host="54.180.124.182",
                               user=ch6_dbconfig.db_user,
                               passwd=ch6_dbconfig.db_password,
                               db=database)
    
    def get_all_inputs(self):
        connection = self.connect()
        try:
            q = "SELECT description FROM crimes;"
            with connection.cursor() as cur:
                cur.execute(q)
            return cur.fetchall()
        finally:
            connection.close()
        
    def add_input(self, data):
        connection = self.connect()
        try:
            q = "INSERT INTO crimes (description) VALUES (%s);"
            with connection.cursor() as cur:
                cur.execute(q)
                connection.commit()
        finally:
            connection.close()
    
    def clear_all(self):
        connection = self.connect()
        try:
            q = "DELETE FROM crimes;"
            with connection.cursor() as cur:
                cur.execute(q)
                connection.commit()
        finally:
            connection.close()