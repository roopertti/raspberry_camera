import datetime
from datetime import date
import sqlite3
from sqlite3 import Error
import json
from picamera import PiCamera
from time import sleep

def read_conf():
    with open('config.json') as config_file:
        data = json.load(config_file)
        return data
    return None

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def fetch_one(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    if len(rows) > 0:
        return rows[0]
    else:
        return None

def insert_one(conn, query, data):
    cur = conn.cursor()
    if data is None:
        cur.execute(query)
    else:
        cur.execute(query, data)
    conn.commit()
    return cur.lastrowid

def get_day_id(conn, today):
    select_query = "SELECT * FROM days WHERE date={}".format(today)
    existing_day = fetch_one(conn, select_query)

    if existing_day is None:
        print("creating new day")
        insert_query = "INSERT INTO days(date) VALUES({});".format(today)
        
        day_id = insert_one(conn, insert_query, None)
        return day_id
    else:
        print("existing day found")
        return existing_day[0]

def save_img_metadata(conn, day_id, filename, captured):
    query = "INSERT INTO photos(day_id, filename, captured) VALUES(?,?,?);"
    data = (day_id, filename, captured)
    photo_id = insert_one(conn, query, data)
    print("Image saved! Id:{}, Filename:{}, Captured:{}".format(photo_id, filename, captured))

def main():
    # Load config vars
    config = read_conf()
    db_path = config["local_db_path"]
    cam_rotation = config["rotation"]
    img_dir = config["img_dir"]

    # Initialize database
    conn = create_connection(db_path)

    # Initialize camera module
    camera = PiCamera()
    camera.rotation = cam_rotation

    # Date and exact timestamp as integer
    today = date.today()
    now = int(datetime.datetime.now().timestamp())

    # Get id of day or create new for reference
    day_id = get_day_id(conn, today)

    # Set filename and capture image
    image_file_name = str(now) + ".jpg"
    new_image_path = img_dir + image_file_name
    camera.capture(new_image_path)

    # Save image "metadata"
    save_img_metadata(conn, day_id, image_file_name, datetime.datetime.now())

main()
