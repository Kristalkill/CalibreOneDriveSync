# utils.py

import os
import time

class Utils:
    
    # Utility class providing logging functionality and file system operations.
    

    def __init__(self, config):
        
        # Initializes the Utils instance.

        # :param config: Configuration object containing settings.
        
        self.config = config
        self.log_file = None  # File object for the log file.

    def open_log(self):
        
        # Opens the log file in append mode if logging is enabled.
        
        if self.config.Log:
            try:
                self.log_file = open("sync.log", "a")
            except IOError as e:
                print(f"Failed to open log file: {e}")
                self.log_file = None

    def close_log(self):
        
        # Closes the log file if it's open.
        
        if self.log_file:
            try:
                self.log_file.close()
            except IOError as e:
                print(f"Failed to close log file: {e}")

    def log(self, message):
        
        # Logs a message with a timestamp to both the console and the log file if logging is enabled.

        # :param message: The message to log.
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {message}"
        print(log_message)
        if self.config.Log and self.log_file:
            try:
                self.log_file.write(log_message + "\n")
            except IOError as e:
                print(f"Failed to write to log file: {e}")

    def get_last_modified_time(self, file_path):
        
        # Retrieves the last modified time of a file.

        # :param file_path: The path to the file.
        # :return: The last modified time as a float (seconds since the epoch), or None if an error occurs.
        
        try:
            return os.path.getmtime(file_path)
        except OSError as e:
            self.log(f"Error getting last modified time for {file_path}: {e}")
            return None
