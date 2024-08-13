# calibre_server.py

import subprocess
import requests

class CalibreServer:
    
    # Manages operations related to the Calibre server, including starting the server and reconnecting.
    

    def __init__(self, util, config):
        
        # Initializes the CalibreServer instance.

        # :param util: Instance of the Utils class for logging.
        # :param config: Configuration object containing settings.
        
        self.util = util
        self.config = config

    def start_server(self):
        
        # Starts the Calibre server using the provided CPS path.
        
        self.util.log("Starting Calibre server...")
        try:
            # Start the Calibre server subprocess.
            subprocess.Popen([self.config.CPSPath, "-r"])
            self.util.log("Calibre server started.")
        except Exception as e:
            self.util.log(f"Failed to start Calibre server: {e}")

    def reconnect(self):
        
        # Sends a request to the Calibre server to reconnect, typically after database changes.
        
        try:
            self.util.log("Attempting to reconnect Calibre server...")
            response = requests.get(f"http://localhost:{self.config.PortCalibreWeb}/reconnect")
            if response.status_code == 200:
                self.util.log("Calibre server reconnected successfully.")
            else:
                self.util.log(f"Failed to reconnect. Status code: {response.status_code}")
        except Exception as e:
            self.util.log(f"Error during reconnection: {str(e)}")
