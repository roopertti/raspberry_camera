import os, shutil
from picamera import PiCamera
import datetime
from time import sleep

class ImageFiles:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def delete_all_images(self):
        for the_file in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    def capture_image(self, cam_settings):
        now = int(datetime.datetime.now().timestamp())
        camera = PiCamera()
        
        for key, value in cam_settings.items():
            setattr(camera, key, value)

        image_file_name = str(now) + ".jpg"
        new_image_path = self.folder_path + image_file_name
        camera.start_preview()
        sleep(3)
        camera.capture(new_image_path)
        camera.stop_preview()

        return { "filename": image_file_name, "captured": now }

    def calc_size_of_images(self):
        list_of_files = os.listdir(self.folder_path)
        total_bytes = 0
        for file in list_of_files:
            path = self.folder_path + file
            size = os.path.getsize(path)
            total_bytes += size
        total_mbs = round(total_bytes / 1024 / 1024, 1)
        print("Amount of images in total: " + str(len(list_of_files)))
        print("Total size of image files: {} MB".format(total_mbs))
    
        
        
