# test_onedrive_server.py

import subprocess
import unittest
from unittest.mock import patch, MagicMock, mock_open

from onedrive_server import OneDriveServer
from utils import Utils
from default_config import default_config
from calibre_server import CalibreServer

class TestOneDriveServer(unittest.TestCase):
    def setUp(self):
        self.config = default_config
        self.utils = Utils(self.config)
        self.calibre_server = CalibreServer(util=self.utils, config=self.config)
        self.onedrive_server = OneDriveServer(util=self.utils, config=self.config, calibre_server=self.calibre_server)

    @patch.object(OneDriveServer, '_execute')
    def test_call_onedrive_success_no_db_change(self, mock_execute):
        
        # Test OneDrive synchronization when there's no change in the metadata database.
        
        mock_execute.return_value = iter(["Syncing...", "Done"])
        self.onedrive_server.last_modified_time = 1625068800.0  # Mocked previous timestamp

        with patch.object(self.utils, 'log') as mock_log, \
             patch.object(self.utils, 'get_last_modified_time', return_value=1625068800.0) as mock_get_mtime, \
             patch.object(self.calibre_server, 'reconnect') as mock_reconnect:
            mock_onFinish = MagicMock()
            self.onedrive_server.call_onedrive(onFinish=mock_onFinish)

            # Verify logs
            mock_log.assert_any_call("Starting OneDrive sync...")
            mock_log.assert_any_call("Syncing...")
            mock_log.assert_any_call("Done")
            mock_log.assert_any_call("OneDrive sync finished.")
            mock_log.assert_any_call("No changes detected in metadata.db. No need to reload CalibreWeb DB.")

            # Verify that reconnect was not called since there was no change
            mock_reconnect.assert_not_called()
            mock_onFinish.assert_called_once()

    @patch.object(OneDriveServer, '_execute')
    def test_call_onedrive_success_with_db_change(self, mock_execute):
        
        # Test OneDrive synchronization when there's a change in the metadata database.
        
        mock_execute.return_value = iter(["Syncing...", "Done"])
        self.onedrive_server.last_modified_time = 1625068800.0  # Mocked previous timestamp

        with patch.object(self.utils, 'log') as mock_log, \
             patch.object(self.utils, 'get_last_modified_time', return_value=1625072400.0) as mock_get_mtime, \
             patch.object(self.calibre_server, 'reconnect') as mock_reconnect:
            mock_onFinish = MagicMock()
            self.onedrive_server.call_onedrive(onFinish=mock_onFinish)

            # Verify logs
            mock_log.assert_any_call("Starting OneDrive sync...")
            mock_log.assert_any_call("Syncing...")
            mock_log.assert_any_call("Done")
            mock_log.assert_any_call("OneDrive sync finished.")
            mock_log.assert_any_call("Changes detected in metadata.db. Reloading CalibreWeb DB...")

            # Verify that reconnect was called
            mock_reconnect.assert_called_once()
            mock_onFinish.assert_called_once()

    @patch.object(OneDriveServer, '_execute', side_effect=subprocess.CalledProcessError(1, ['onedrive', '--synchronize']))
    def test_call_onedrive_failure(self, mock_execute):
        
        # Test handling of a failure during OneDrive synchronization.
        
        with patch.object(self.utils, 'log') as mock_log:
            mock_onFinish = MagicMock()
            self.onedrive_server.call_onedrive(onFinish=mock_onFinish)

            # Verify logs
            mock_log.assert_any_call("Starting OneDrive sync...")
            mock_log.assert_any_call("OneDrive sync failed: Command '['onedrive', '--synchronize']' returned non-zero exit status 1.")

            # Verify that onFinish was not called due to failure
            mock_onFinish.assert_not_called()

    @patch("subprocess.Popen")
    def test_execute_success(self, mock_popen):
        
        #Test successful execution of a shell command.
        
        process_mock = MagicMock()
        attrs = {'stdout.readline.side_effect': ['line1\n', 'line2\n', '']}
        process_mock.configure_mock(**attrs)
        process_mock.returncode = 0
        mock_popen.return_value = process_mock

        output = list(self.onedrive_server._execute(['some', 'command']))
        self.assertEqual(output, ['line1', 'line2'])
        mock_popen.assert_called_with(['some', 'command'], stdout=subprocess.PIPE, universal_newlines=True)

    @patch("subprocess.Popen")
    def test_execute_failure(self, mock_popen):
        
        #Test handling of a failure during execution of a shell command.
        
        process_mock = MagicMock()
        attrs = {'stdout.readline.side_effect': ['error line\n', '']}
        process_mock.configure_mock(**attrs)
        process_mock.returncode = 1
        mock_popen.return_value = process_mock

        with self.assertRaises(subprocess.CalledProcessError):
            output = list(self.onedrive_server._execute(['some', 'command']))

if __name__ == '__main__':
    unittest.main()
