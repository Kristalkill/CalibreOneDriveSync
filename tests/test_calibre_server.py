# test_calibre_server.py

import unittest
from unittest.mock import patch, MagicMock

from calibre_server import CalibreServer
from utils import Utils
from default_config import default_config

class TestCalibreServer(unittest.TestCase):
    def setUp(self):
        self.config = default_config
        self.utils = Utils(self.config)
        self.calibre_server = CalibreServer(util=self.utils, config=self.config)

    @patch("subprocess.Popen")
    def test_start_server_success(self, mock_popen):
        
        #Test starting the Calibre server successfully.
        
        with patch.object(self.utils, 'log') as mock_log:
            self.calibre_server.start_server()
            mock_popen.assert_called_with([self.config.CPSPath, "-r"])
            mock_log.assert_any_call("Starting Calibre server...")
            mock_log.assert_any_call("Calibre server started.")

    @patch("subprocess.Popen", side_effect=Exception("Popen failed"))
    def test_start_server_failure(self, mock_popen):
        
        #Test handling of an error when starting the Calibre server.
        
        with patch.object(self.utils, 'log') as mock_log:
            self.calibre_server.start_server()
            mock_log.assert_any_call("Starting Calibre server...")
            mock_log.assert_any_call("Failed to start Calibre server: Popen failed")

    @patch("requests.get")
    def test_reconnect_success(self, mock_get):
        
        #Test successful reconnection to the Calibre server.
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch.object(self.utils, 'log') as mock_log:
            self.calibre_server.reconnect()
            mock_get.assert_called_with(f"http://localhost:{self.config.PortCalibreWeb}/reconnect")
            mock_log.assert_any_call("Attempting to reconnect Calibre server...")
            mock_log.assert_any_call("Calibre server reconnected successfully.")

    @patch("requests.get")
    def test_reconnect_failure_status_code(self, mock_get):
        
        #Test handling of a failed reconnection due to a bad status code.
        
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with patch.object(self.utils, 'log') as mock_log:
            self.calibre_server.reconnect()
            mock_get.assert_called_with(f"http://localhost:{self.config.PortCalibreWeb}/reconnect")
            mock_log.assert_any_call("Attempting to reconnect Calibre server...")
            mock_log.assert_any_call("Failed to reconnect. Status code: 500")

    @patch("requests.get", side_effect=Exception("Connection error"))
    def test_reconnect_exception(self, mock_get):
        
        #Test handling of an exception during reconnection.
        
        with patch.object(self.utils, 'log') as mock_log:
            self.calibre_server.reconnect()
            mock_get.assert_called_with(f"http://localhost:{self.config.PortCalibreWeb}/reconnect")
            mock_log.assert_any_call("Attempting to reconnect Calibre server...")
            mock_log.assert_any_call("Error during reconnection: Connection error")

if __name__ == '__main__':
    unittest.main()
