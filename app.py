#!/usr/bin/env python3
import os
from database import ImageDatabase
from imagefiles import ImageFiles
import sys
import json

class Program:
    def __init__(self):
        local_path = os.path.dirname(os.path.realpath(__file__))
        self.local_path = local_path
        db_path = local_path + '/db/'
        image_folder_path = local_path + '/images/'

        if not os.path.exists(db_path):
            os.makedirs(db_path)

        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)
        
        database = ImageDatabase(db_path)
        database.create_connection()
        self.db = database
        
        image_file_module = ImageFiles(image_folder_path)
        self.image_files = image_file_module

    def read_camera_settings(self):
        camera_settings_path = self.local_path + '/camera.json'
        with open(camera_settings_path) as config_file:
            data = json.load(config_file)
            return data
        return None
        

    def reset(self):
        print("Resetting database...")
        self.db.reset_tables()
        print("Removing image files...")
        self.image_files.delete_all_images()

    def capture(self):
        try:
            print("Capturing image...")
            cam_settings = self.read_camera_settings()
            if cam_settings is not None:
                capture_details = self.image_files.capture_image(cam_settings)
                day_id = self.db.get_day_id()
                self.db.save_img_metadata(day_id, capture_details["filename"], capture_details["captured"])
                print("Success")
        except Exception as e:
            print(e)

    def stats(self):
        self.db.print_totals_per_day()
        self.image_files.calc_size_of_images()
        

def reset():
    program.reset()

def test():
    print("Hello")

def capture():
    program.capture()

def stats():
    program.stats()

def give_help():
    print("List of arguments:")
    print("  reset    -  Clears all image files and resets the database.")
    print("  test     -  Test command.")
    print("  capture  -  Capture image and save it's metadata to the database.")
    print("  help     -  See this list of arguments again.")

program = Program()

options = {
    "reset": reset,
    "test": test,
    "capture": capture,
    "stats": stats,
    "help": give_help
}

if len(sys.argv) == 1:
    capture()
else:
    arg = sys.argv[1]
    try:
        options[arg]()
    except KeyError as e:
        print("Argument not recognized")
        give_help()




    
    

    
