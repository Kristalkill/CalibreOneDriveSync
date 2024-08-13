# onedrive_server.py

import subprocess

class OneDriveServer:
    
    # Manages synchronization with OneDrive and monitors changes in the Calibre metadata database.
    

    def __init__(self, util, config, calibre_server):
        
        # Initializes the OneDriveServer instance.

        # :param util: Instance of the Utils class for logging and utility functions.
        # :param config: Configuration object containing settings.
        # :param calibre_server: Instance of the CalibreServer to manage Calibre operations.
        
        self.util = util
        self.config = config
        self.calibre_server = calibre_server
        self.last_modified_time = None  # Tracks the last modification time of the metadata.db

    def call_onedrive(self, onFinish):
        
        # Initiates the OneDrive synchronization process. After syncing, it checks if the Calibre metadata database has changed and reloads the Calibre server if necessary.

        # :param onFinish: Callback function to execute upon completion.
        
        self.util.log("Starting OneDrive sync...")
        try:
            # Execute the OneDrive synchronization command and log its output.
            for output in self._execute(["onedrive", "--synchronize"]):
                self.util.log(output.strip())
            self.util.log("OneDrive sync finished.")
        except subprocess.CalledProcessError as e:
            self.util.log(f"OneDrive sync failed: {e}")
            return
        
        # Check for changes in the metadata database and reload Calibre if needed.
        self._check_and_reload_calibre()
        onFinish()

    def _execute(self, cmd):
        
        # Executes a shell command and yields its output line by line.

        # :param cmd: List of command arguments to execute.
        # :return: Generator yielding output lines from the command.
        # :raises subprocess.CalledProcessError: If the command exits with a non-zero status.
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        if process.stdout:
            for stdout_line in iter(process.stdout.readline, ""):
                yield stdout_line.strip()
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, cmd)

    def _check_and_reload_calibre(self):
        
        # Checks if the Calibre metadata database has been modified since the last check.
        # If changes are detected, instructs the Calibre server to reconnect.
        
        current_modified_time = self.util.get_last_modified_time(self.config.MetadataDBPath)
        
        if current_modified_time is None:
            self.util.log("Could not determine the last modified time of the metadata database.")
            return

        # If it's the first check or if the database has been modified since the last check.
        if self.last_modified_time is None or current_modified_time > self.last_modified_time:
            self.util.log("Changes detected in metadata.db. Reloading CalibreWeb DB...")
            self.calibre_server.reconnect()
            self.last_modified_time = current_modified_time
        else:
            self.util.log("No changes detected in metadata.db. No need to reload CalibreWeb DB.")
