# main.py

import sched
import time
import subprocess

from src.utils import Utils
from src.calibre_server import CalibreServer
from src.onedrive_server import OneDriveServer
from src.default_config import default_config

def kill_process_at_port(portnumber):
    
    # Terminates any process currently listening on the specified TCP port.

    # :param portnumber: The port number to clear.
    
    subprocess.call(["fuser", "-k", f"{portnumber}/tcp"])

def main():
    
    # Entry point of the application. Initializes components and starts the synchronization scheduler.
    
    print(f"Start, clearing process at port {default_config.PortCalibreWeb}")
    kill_process_at_port(default_config.PortCalibreWeb)
    
    # Initialize utility, Calibre server, and OneDrive server instances.
    my_utils = Utils(default_config)
    my_calibre_server = CalibreServer(util=my_utils, config=default_config)
    my_onedrive_server = OneDriveServer(util=my_utils, config=default_config, calibre_server=my_calibre_server)
    my_calibre_server.start_server()
    
    def scheduled_task(schedule):
        #Task scheduled to run at regular intervals. Handles OneDrive synchronization and checks for updates in the Calibre metadata database.

        #:param schedule: The scheduler instance managing task timings.
        
        def schedule_next_process():
            
            # Schedules the next execution of the scheduled_task after a specified interval.
            
            my_utils.close_log()
            schedule.enter(default_config.TimeCheckOneDriveSecond, 1, scheduled_task, (schedule,))
    
        if default_config.Log:
            my_utils.open_log()
    
        my_onedrive_server.call_onedrive(onFinish=schedule_next_process)
    
    # Start the scheduler
    my_scheduler = sched.scheduler(time.time, time.sleep)
    # Schedule the first execution of the scheduled_task
    my_scheduler.enter(default_config.TimeCheckOneDriveSecond, 1, scheduled_task, (my_scheduler,))
    my_scheduler.run()

if __name__ == "__main__":
    main()
