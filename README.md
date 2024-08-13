# CalibreOneDriveSync

CalibreOneDriveSync is a Python project designed to synchronize a Calibre library with OneDrive and automatically reload the CalibreWeb database when changes in the metadata are detected. It helps keep your Calibre library updated with changes in OneDrive and ensures the CalibreWeb DB is refreshed accordingly.

## Features

- Synchronizes Calibre library with OneDrive.
- Detects changes in the `metadata.db` file and triggers a reload of the CalibreWeb DB.
- Configurable intervals for synchronization and checks.
- Logging and error handling.

## Prerequisites

- Python 3.8 or later

## Installation

1. **Install [Calibre-Web](https://github.com/janeczku/calibre-web)**
2. **Install OneDrive**

    Linux - [abraunegg/onedrive](https://github.com/abraunegg/onedrive)

    Windows (My app doesn't work for Windows right now) 

3. **Clone the Repository:**

    ```bash
    git clone https://github.com/Kristalkill/CalibreOneDriveSync.git
    cd CalibreOneDriveSync
    ```

4. **Install Dependencies Using Poetry**

    *With requirements.txt*
    ```bash
    pip install -r requirements.txt
    ```

    *With Poetry. Make sure it is installed. If not, install it by following the [Poetry installation](https://python-poetry.org/docs/) instructions.*
    ```bash
    poetry install
    ```

5. **Setup .env or default_config.py**
    
    ```env
    METADATA_DB_PATH: Path to the metadata.db file in your Calibre library.
    CPS_PATH: Path to the Calibre server script.
    PORT_CALIBRE_WEB: ~~Port number for the Calibre content server.~~ Currently left it 8083
    TIME_CHECK_ONEDRIVE_SECOND: Interval in seconds to check for changes in OneDrive.
    LOG: Enable or disable logging (True or False).
    ```

6. **Run script**
    
    *With python*
    ```bash
    python3 main.pu
    ```

    *With Poetry*
    ```
    poetry run python main.py
    ```

7. Systemd Service Setup (Optional for Linux):

    Create a user systemd service file
    ```bash
    mkdir -p ~/.config/systemd/user
    sudo nano ~/.config/systemd/user/calibre-onedrive-sync.service
    ```
    Then paste this and edit it
    ```ini
    [Unit]
    Description=Calibre OneDrive Sync Service
    After=network.target

    [Service]
    ExecStart=/path/to/poetry/or/python /path/to/CalibreOneDriveSync/main.py
    WorkingDirectory=/path/to/CalibreOneDriveSync
    Restart=always
    User=your-username

    [Install]
    WantedBy=default.target
    ```

    Usage
    ```bash
    systemctl --user daemon-reload
    systemctl --user enable calibre-onedrive-sync.service
    systemctl --user start calibre-onedrive-sync.service
    ```
    **Or you can create global service**
    ```bash
    sudo nano /etc/systemd/system/calibre-onedrive-sync.service
    ```
    Then paste this and edit it
    ```ini
    [Unit]
    Description=Calibre OneDrive Sync
    After=network.target

    [Service]
    ExecStart=/path/to/poetry/or/python /path/to/CalibreOneDriveSync/main.py
    WorkingDirectory=/path/to/CalibreOneDriveSync
    Restart=always
    User=your-username

    [Install]
    WantedBy=multi-user.target
    ```
    Usage
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start calibre-onedrive-sync
    sudo systemctl enable calibre-onedrive-sync
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

I welcome contributions from the community! To contribute to this project, please follow these steps:

1. **Fork the Repository:** 

    ```
    Click the "Fork" button on the top right of the repository page.
    ```

2. **Clone Your Fork:**

    ```bash
    git clone https://github.com/yourname/CalibreOneDriveSync.git
    ```
3. **Create a New Branch:**

    ```bash
    git checkout -b feature-branch
    ```

4. **Implement your changes or add a new feature.**

5. **Commit Your Changes:**

    ```bash
    git add .
    git commit -m "Describe your changes"
    ```
6. **Push to Your Fork:**

    ```bash
    git push origin feature-branch
    ```

7. **Create a Pull Request: Go to the original repository and submit a pull request with your changes.**

