#!/usr/bin/env python3
import os
from database import ImageDatabase
from imagefiles import ImageFiles
import sys
import json
import traceback
from logger import Logger

class Program:
    """Starting point class for camera CLI"""
    def __init__(self):
        """Initialize ImageDatabase- and ImageFiles-classes"""

        
        # Set correct paths
        local_path = os.path.dirname(os.path.realpath(__file__))
        self.local_path = local_path

        # Init ImageDatabase class
        database = ImageDatabase()
        database.create_connection()
        self.db = database

        # Init ImageFiles class
        image_file_module = ImageFiles()
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
        Logger.info("Resetting database...")
        self.db.reset_tables()
        Logger.info("Removing image files...")
        self.image_files.delete_all_images()

    def capture(self):
        """
        Captures an image with given settings
        Saves metadata of file to database
        """
        try:
            print("Reading camera settings...")
            cam_settings = self.read_camera_settings()
            if cam_settings is not None:
                print("Camera settings were succesfully read! Capturing image...")
                capture_details = self.image_files.capture_image(cam_settings)
                # Set reference to day-table from image-table and save image metadata
                day_id = self.db.get_day_id()
                self.db.save_img_metadata(day_id, capture_details["filename"], capture_details["captured"])
                Logger.capture("Image captured! Filename: {} Captured: {}".format(capture_details["filename"], capture_details["captured"]))
        except Exception as e:
            Logger.error("Error with capture", traceback.format_exc())

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
