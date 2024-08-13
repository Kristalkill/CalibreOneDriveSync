import unittest
from unittest.mock import patch, mock_open
import os

from utils import Utils
from default_config import default_config

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Create a config object with logging enabled
        self.config = default_config
        self.config.Log = True
        self.utils = Utils(self.config)

    @patch("builtins.open", new_callable=mock_open)
    def test_open_log_success(self, mock_file):
        
        #Test that the log file opens successfully.
        
        self.utils.open_log()
        mock_file.assert_called_with("sync.log", "a")
        self.assertIsNotNone(self.utils.log_file)

    @patch("builtins.open", side_effect=IOError("Cannot open file"))
    def test_open_log_failure(self, mock_file):
        
        #Test handling of an error when opening the log file.
        
        with patch('builtins.print') as mock_print:
            self.utils.open_log()
            mock_print.assert_called_with("Failed to open log file: Cannot open file")
            self.assertIsNone(self.utils.log_file)

    @patch("builtins.open", new_callable=mock_open)
    def test_close_log_success(self, mock_file):
        
        #Test that the log file closes successfully.
        
        self.utils.open_log()
        self.utils.close_log()
        if(self.utils.log_file):
            self.assertTrue(self.utils.log_file.closed)

    def test_close_log_no_file(self):
        
        #Test closing the log file when it's not open.
        
        with patch('builtins.print') as mock_print:
            self.utils.close_log()
            # No print should occur since log_file is None
            mock_print.assert_not_called()

    @patch("time.strftime", return_value="2023-08-15 12:00:00")
    def test_log(self, mock_strftime):
        
        #Test the logging functionality, ensuring messages are logged with timestamps.
        
        with patch('builtins.print') as mock_print, \
             patch("builtins.open", mock_open()) as mock_file:
            self.utils.open_log()
            self.utils.log("Test message")
            mock_print.assert_called_with("2023-08-15 12:00:00 - Test message")
            mock_file().write.assert_called_with("2023-08-15 12:00:00 - Test message\n")

    @patch("os.path.getmtime", return_value=1625068800.0)  # Mocked timestamp
    def test_get_last_modified_time_success(self, mock_getmtime):
        
        #Test retrieving the last modified time of a file successfully.
        
        modified_time = self.utils.get_last_modified_time("/path/to/file")
        self.assertEqual(modified_time, 1625068800.0)
        mock_getmtime.assert_called_with("/path/to/file")

    @patch("os.path.getmtime", side_effect=OSError("File not found"))
    def test_get_last_modified_time_failure(self, mock_getmtime):
        
        #Test handling of an error when retrieving the last modified time.
        
        with patch.object(self.utils, 'log') as mock_log:
            modified_time = self.utils.get_last_modified_time("/path/to/nonexistent/file")
            self.assertIsNone(modified_time)
            mock_log.assert_called_with("Error getting last modified time for /path/to/nonexistent/file: File not found")

if __name__ == '__main__':
    unittest.main()
