from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    # Port number for the Calibre content server
    PortCalibreWeb = int(os.getenv('PORT_CALIBRE_WEB', 8083))
    
    # Time interval in seconds to check for changes in OneDrive
    TimeCheckOneDriveSecond = int(os.getenv('TIME_CHECK_ONEDRIVE_SECOND', 60))

    # Path to the metadata.db file in your Calibre library
    MetadataDBPath = os.getenv('METADATA_DB_PATH', "path/to/metadata.db")

    # Path to the cps file in your venv
    CPSPath = os.getenv('CPS_PATH', "path/to/cps")

    # Enable or disable logging
    Log = os.getenv('LOG', 'True').lower() in ('true', '1', 'yes')

default_config = Config()