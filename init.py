import sqlite3
from sqlite3 import Error
import json

def read_conf():
    with open('config.json') as config_file:
        data = json.load(config_file)
        local_db_path = data["local_db_path"]
        return local_db_path
    return None

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def commit_query(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def main():
    database_path = read_conf()
    sql_clear_day = "DROP TABLE IF EXISTS days;"
    sql_clear_photos = "DROP TABLE IF EXISTS photos;"
    sql_create_day = """CREATE TABLE days (
        id integer PRIMARY KEY,
        date text NOT NULL
    );"""
    sql_create_photos = """CREATE TABLE photos (
        id integer PRIMARY KEY,
        day_id integer NOT NULL,
        filename text NOT NULL,
        captured text NOT NULL,
        FOREIGN KEY (day_id) REFERENCES days(id)
    );"""

    conn = create_connection(database_path)
    if conn is not None:
        commit_query(conn, sql_clear_day)
        commit_query(conn, sql_clear_photos)
        commit_query(conn, sql_create_day)
        commit_query(conn, sql_create_photos)
    else:
        print("Error: No database connection")
        
 
if __name__ == '__main__':
    main()
