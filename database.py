import sqlite3
from sqlite3 import Error
from datetime import date
import os
from pathlib import Path
from logger import Logger
import traceback

class ImageDatabase:
    """Handles queries to sqlite database"""

    def __init__(self):
        local_path = os.path.dirname(os.path.realpath(__file__))
        self.db_path = local_path + '/db/database.db'

        # Create folder with db file for db if there is no folder
        if not os.path.exists(self.db_path):
            raise Exception("No db file, create new to ./db/database.db and run './cli.py reset'")
    
    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            self.conn = conn
        except Error as e:
            Logger.error("Error while connecting to database", traceback.format_exc())
            self.conn = None

    # BASIC DATABASE QUERIES

    def exec_query_void(self, sql):
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Error as e:
            Logger.error("Error with void query", traceback.format_exc())

    def fetch_one(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()

            if len(rows) > 0:
                return rows[0]
            else:
                return None
        except Error as e:
            Logger.error("Error with fetch one query", traceback.format_exc())

    def fetch_many(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()

            return rows
        except Error as e:
            Logger.error("Error with fetch many query", traceback.format_exc())

    def insert_one(self, query, data):
        try:
            cur = self.conn.cursor()
            if data is None:
                cur.execute(query)
            else:
                cur.execute(query, data)
            self.conn.commit()
            return cur.lastrowid
        except Error as e:
            Logger.error("Error with insert query", traceback.format_exc())

    # CUSTOM FUNCTIONS

    def reset_tables(self):
        sql_clear_day = "DROP TABLE IF EXISTS days;"
        sql_clear_images = "DROP TABLE IF EXISTS images;"
        sql_create_day = """CREATE TABLE days (
            id integer PRIMARY KEY,
            date text NOT NULL
        );"""
        sql_create_images = """CREATE TABLE images (
            id integer PRIMARY KEY,
            day_id integer NOT NULL,
            filename text NOT NULL,
            captured text NOT NULL,
            FOREIGN KEY (day_id) REFERENCES days(id)
        );"""

        print("Clearing days...")
        self.exec_query_void(sql_clear_day)
        print("Clearing images...")
        self.exec_query_void(sql_clear_images)
        print("Creating days table...")
        self.exec_query_void(sql_create_day)
        print("Creating images table...")
        self.exec_query_void(sql_create_images)

    def get_day_id(self):
        today = date.today()
        select_query = "SELECT * FROM days WHERE date='{}'".format(today)
        existing_day = self.fetch_one(select_query)

        if existing_day is None:
            Logger.info("Creating new day to database...")
            insert_query = "INSERT INTO days(date) VALUES('{}');".format(today)
            day_id = self.insert_one(insert_query, None)
            return day_id
        else:
            return existing_day[0]

    def save_img_metadata(self, day_id, filename, captured):
        query = "INSERT INTO images(day_id, filename, captured) VALUES(?,?,?);"
        data = (day_id, filename, captured)
        photo_id = self.insert_one(query, data)
        print("Image metadata saved Id:{}, Filename:{}, Captured:{}".format(photo_id, filename, captured))

    def print_totals_per_day(self):
        select_query = """SELECT days.date, COUNT(images.id)
                            FROM days
                            INNER JOIN images
                            ON images.day_id = days.id GROUP BY days.date;"""

        rows = self.fetch_many(select_query)
        for row in rows:
            print("Images captured on {}: {}".format(row[0], row[1]))

