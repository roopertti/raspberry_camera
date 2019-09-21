import os, shutil
from picamera import PiCamera
from datetime import datetime, date
from time import sleep
from logger import Logger
import traceback
from functools import reduce
from PIL import Image

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

    def print_details(self):
        try:
            list_of_subfolders = self.get_full_paths_of_folder_contents()
            total_bytes = 0
            total_amount = 0
            if len(list_of_subfolders) > 0:
                print("Image folder has footage over {} days in total.".format(len(list_of_subfolders)))
            for subfolder_path in list_of_subfolders:
                list_of_images = self.get_full_paths_of_folder_contents(subfolder_path)
                total_amount += len(list_of_images)
                print("{}: {} images in total".format(os.path.basename(subfolder_path), len(list_of_images)))
                total_bytes += self.get_subfolder_size(subfolder_path)
            total_mbs = round(total_bytes / 1024 / 1024, 1)
            print("Amount of images in total: " + str(total_amount))
            print("Total size of image files: {} MB".format(total_mbs))
        except Exception:
            Logger.error("Error while calculating image sizes", traceback.format_exc())

    def get_full_paths_of_folder_contents(self, subfolder_path = None):
        if subfolder_path is None:
            return [os.path.join(self.folder_path, sub_path) for sub_path in os.listdir(self.folder_path)]
        else:
            return [os.path.join(subfolder_path, image_path) for image_path in os.listdir(subfolder_path)]

    def get_subfolder_size(self, subfolder_path):
        image_paths = self.get_full_paths_of_folder_contents(subfolder_path)
        image_sizes = [os.path.getsize(img) for img in image_paths]
        subfolder_size_total = reduce(lambda x, y: x + y, image_sizes)
        return subfolder_size_total

    def get_image_details(self, image_path):
        return { 
            'image_size_mb': round(os.path.getsize(image_path) / 1024 / 1024, 1),
            'filename': os.path.basename(image_path),
            'resolution': self.read_image_resolution(image_path)
        }

    def read_image_resolution(self, image_path):
        image = Image.open(image_path)
        return "{}x{}".format(image.size[0], image.size[1])

    def fetch_image_details_api(self):
        response = []
        subfolders = self.get_full_paths_of_folder_contents()
        for subfolder in subfolders:
            subfolder_size = round(self.get_subfolder_size(subfolder) / 1024 / 1024, 1)
            subfolder_name = os.path.basename(subfolder)
            image_files = self.get_full_paths_of_folder_contents(subfolder)
            folder_obj = {
                'folder_name': subfolder_name,
                'folder_size_mb': subfolder_size,
                'images': [self.get_image_details(img) for img in image_files]
            }
            response.append(folder_obj)
        return response


