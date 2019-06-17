#!/usr/bin/env python3
import os
from database import ImageDatabase
from imagefiles import ImageFiles
import sys
import json

class Program:
    """Starting point class for camera CLI"""
    def __init__(self):
        """Initialize ImageDatabase- and ImageFiles-classes"""

        # Set correct paths
        local_path = os.path.dirname(os.path.realpath(__file__))
        self.local_path = local_path
        db_path = local_path + '/db/'
        image_folder_path = local_path + '/images/'

        # Create folder for db if there is no folder
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        # Create folder for images if there is no folder
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)

        # Init ImageDatabase class
        database = ImageDatabase(db_path)
        database.create_connection()
        self.db = database

        # Init ImageFiles class
        image_file_module = ImageFiles(image_folder_path)
        self.image_files = image_file_module

    def read_camera_settings(self):
        """
        Read PiCamera settings from camera.json file and return them
        Return None if no file is present
        """
        camera_settings_path = self.local_path + '/camera.json'
        with open(camera_settings_path) as config_file:
            data = json.load(config_file)
            return data
        return None
        

    def reset(self):
        """
        Drops database tables and creates them again
        Removes all files from /images subfolder
        """
        print("Resetting database...")
        self.db.reset_tables()
        print("Removing image files...")
        self.image_files.delete_all_images()

    def capture(self):
        """
        Captures an image with given settings
        Saves metadata of file to database
        """
        try:
            print("Capturing image...")
            cam_settings = self.read_camera_settings()
            if cam_settings is not None:
                capture_details = self.image_files.capture_image(cam_settings)
                # Set reference to day-table from image-table and save image metadata
                day_id = self.db.get_day_id()
                self.db.save_img_metadata(day_id, capture_details["filename"], capture_details["captured"])
                print("Success")
        except Exception as e:
            print(e)

    def stats(self):
        """Print statistics about images"""
        self.db.print_totals_per_day()
        self.image_files.calc_size_of_images()

def give_help():
    """List all arguments to command line"""
    print("List of arguments:")
    print("  reset    -  Clears all image files and resets the database.")
    print("  capture  -  Capture image and save it's metadata to the database.")
    print("  stats    -  Print statistics about images")
    print("  help     -  See this list of arguments again.")

# Initialize program
program = Program()

# Map command line arguments to methods and functions
options = {
    "reset": program.reset,
    "capture": program.capture,
    "stats": program.stats,
    "help": give_help
}

# Handle command line arguments
if len(sys.argv) == 1:
    program.capture()
else:
    arg = sys.argv[1]
    try:
        options[arg]()
    except KeyError as e:
        print("Argument not recognized")
        give_help()
