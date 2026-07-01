import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from m365_connector import (
    M365Client,
    build_m365_context,
    load_m365_config,
    save_m365_config,
)


class M365ConnectorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_m365_client_no_token_not_configured(self):
        client = M365Client(token=None)
        self.assertFalse(client.is_configured())

    def test_m365_client_with_token_configured(self):
        client = M365Client(token="fake_token_xyz")
        self.assertTrue(client.is_configured() if client.token else False)

    def test_save_and_load_m365_config(self):
        config = {
            "teams": [{"team_id": "T123", "channel_id": "C456"}],
            "enabled": True,
        }
        save_m365_config(config)
        loaded = load_m365_config()
        self.assertEqual(loaded, config)

    def test_build_m365_context_handles_no_token(self):
        context = build_m365_context()
        self.assertIn("not configured", context.lower())

    @patch("m365_connector.M365Client")
    def test_build_m365_context_with_mock(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.is_configured.return_value = True
        mock_client.get_recent_emails.return_value = [
            {"from": "alice@example.com", "subject": "Project update", "timestamp": "2026-06-23T10:00Z"}
        ]
        mock_client.get_calendar_events.return_value = [
            {"subject": "Team standup", "start": "2026-06-23T09:00Z", "attendees": 5}
        ]
        mock_client_class.return_value = mock_client

        context = build_m365_context()
        self.assertIn("microsoft 365", context.lower())

    def test_m365_client_headers_include_auth(self):
        client = M365Client(token="test_token_123")
        headers = client._headers()
        self.assertIn("Authorization", headers)
        self.assertIn("Bearer", headers["Authorization"])

    def test_m365_client_returns_empty_lists_when_not_configured(self):
        client = M365Client(token=None)
        self.assertEqual(client.get_recent_emails(), [])
        self.assertEqual(client.get_calendar_events(), [])
        self.assertEqual(client.get_onedrive_recent_files(), [])


if __name__ == "__main__":
    unittest.main()
