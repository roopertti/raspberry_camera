import os, shutil
from picamera import PiCamera
from datetime import datetime, date
from time import sleep
from logger import Logger
import traceback

class ImageFiles:
    def __init__(self):
        try:
            local_path = os.path.dirname(os.path.realpath(__file__))
            self.folder_path = os.path.join(local_path, 'images')

            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
        except Exception:
            Logger.error("Error while creating ImageFiles instance", traceback.format_exc())

    def delete_all_images(self):
        try:
            for image_subfolder in os.listdir(self.folder_path):
                complete_path_to_subfolder = os.path.join(self.folder_path, image_subfolder)
                for image_file in os.listdir(complete_path_to_subfolder):
                    complete_path_to_file = os.path.join(complete_path_to_subfolder, image_file)
                    if os.path.isfile(complete_path_to_file):
                        os.unlink(complete_path_to_file)
                os.rmdir(complete_path_to_subfolder)
            os.rmdir(self.folder_path)
        except Exception:
            Logger.error("Error while deleting images", traceback.format_exc())

    def get_current_date_subfolder(self):
        try:
            subfolder_name = str(date.today())
            image_subfolder_path = os.path.join(self.folder_path, subfolder_name)

            if not os.path.exists(image_subfolder_path):
                os.makedirs(image_subfolder_path)
        
            return image_subfolder_path
        except Exception:
            Logger.error("Error while resolving current image subfolder path", traceback.format_exc())

    def capture_image(self, cam_settings):
        try:
            now = int(datetime.now().timestamp())
            formatted_time_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            camera = PiCamera()
        
            for key, value in cam_settings.items():
                if isinstance(value, list):
                    setattr(camera, key, tuple(value))
                else:
                    setattr(camera, key, value)
            
            camera.annotate_text = formatted_time_str
            subfolder_path = self.get_current_date_subfolder()
            image_file_name = str(now) + ".jpg"
            new_image_path = os.path.join(subfolder_path, image_file_name)
            camera.start_preview()
            sleep(3)
            camera.capture(new_image_path)
            camera.stop_preview()

            return { "filename": image_file_name, "captured": formatted_time_str }
        except Exception:
            Logger.error("Error while capturing image", traceback.format_exc())

    def calc_size_of_images(self):
        try:
            list_of_subfolders = os.listdir(self.folder_path)
            total_bytes = 0
            total_amount = 0
            if len(list_of_subfolders) > 0:
                print("Image folder has footage over {} days in total.".format(len(list_of_subfolders)))
            for subfolder in list_of_subfolders:
                complete_subfolder_path = os.path.join(self.folder_path, subfolder)
                list_of_images = os.listdir(complete_subfolder_path)
                total_amount += len(list_of_images)
                print("{}: {} images in total".format(subfolder, len(list_of_images)))
                for image_file in list_of_images:
                    path = os.path.join(complete_subfolder_path, image_file)
                    size = os.path.getsize(path)
                    total_bytes += size
            total_mbs = round(total_bytes / 1024 / 1024, 1)
            print("Amount of images in total: " + str(total_amount))
            print("Total size of image files: {} MB".format(total_mbs))
        except Exception:
            Logger.error("Error while calculating image sizes", traceback.format_exc())
    
        
        
