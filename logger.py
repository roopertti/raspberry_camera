import os
from datetime import date, datetime
from pathlib import Path
import traceback

log_types = { 'info': 'INFO', 'error': 'ERROR', 'capture': 'CAPTURE' }

class Logger:

    @staticmethod
    def get_current_rotation_path():
        now = date.today()
        log_folder_path = os.path.dirname(os.path.realpath(__file__)) + '/camera_log/'
        log_file_path = log_folder_path + str(now) + '.log'
        
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)

        if not os.path.exists(log_file_path):
            Path(log_file_path).touch()

        return log_file_path

    @staticmethod
    def create_log_entry(message, log_type = 'info', stacktrace = None):
        log_file_path = Logger.get_current_rotation_path()
        print(message)
 
        with open(log_file_path, "a") as log_file:
            formatted_stamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            initial_log_row = "{} - {}: {} \n".format(formatted_stamp, log_types[log_type], message)
            log_file.write(initial_log_row)

            if stacktrace is not None:
                log_file.write("-- Stack trace from application error --\n")
                log_file.write(stacktrace + "\n")
                log_file.write("-- End of stack trace --\n")

    @staticmethod
    def info(message):
        Logger.create_log_entry(message)

    @staticmethod
    def capture(message):
        Logger.create_log_entry(message, "capture")

    @staticmethod
    def error(message, stacktrace):
        stack = traceback
        Logger.create_log_entry(message, "error",stacktrace)

    @staticmethod
    def clear_logs():
        log_path = os.path.dirname(os.path.realpath(__file__))

        for log_file in os.listdir(log_path):
            file_path = os.path.join(log_path, log_path)
            try:
                if os.path.isFile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

