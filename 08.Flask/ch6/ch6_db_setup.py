import pymysql
import ch6_dbconfig
connection = pymysql.connect(host="54.180.124.182",
                            user=ch6_dbconfig.db_user,
                            passwd=ch6_dbconfig.db_password)
try:
    with connection.cursor() as cur:
        query = """
        CREATE DATABASE IF NOT EXISTS crimemap;
        """
        cur.execute(query)
        query="""
        CREATE TABLE IF NOT EXISTS crimemap.crimes (
        id int NOT NULL AUTO_INCREMENT,
        latitude FLOAT(10,6),
        longitude FLOAT(10,6),
        date DATETIME,
        category VARCHAR(50),
        description VARCHAR(1000),
        updated_at TIMESTAMP,
        PRIMARY KEY (id)
        )
        """
        cur.execute(query)
        connection.commit()
finally:
    connection.close()
