import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from slack_connector import (
    build_slack_context,
    extract_action_items,
    extract_decisions,
    count_threaded_discussions,
    load_channel_config,
    save_channel_config,
)


class SlackConnectorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_extract_action_items_finds_keywords(self):
        messages = [
            {"user": "alice", "text": "We have an urgent issue with the database", "timestamp": "123", "thread_ts": None},
            {"user": "carol", "text": "TODO: Update the docs", "timestamp": "125", "thread_ts": None},
        ]
        items = extract_action_items(messages)
        self.assertEqual(len(items), 2)

    def test_extract_decisions_finds_keywords(self):
        messages = [
            {"user": "alice", "text": "We decided to use Docker", "timestamp": "123", "thread_ts": None},
            {"user": "bob", "text": "Random chat", "timestamp": "124", "thread_ts": None},
            {"user": "carol", "text": "Approved the budget increase", "timestamp": "125", "thread_ts": None},
        ]
        decisions = extract_decisions(messages)
        self.assertEqual(len(decisions), 2)

    def test_count_threaded_discussions_counts_threads(self):
        messages = [
            {"user": "alice", "text": "msg1", "timestamp": "123", "thread_ts": None},
            {"user": "bob", "text": "msg2", "timestamp": "124", "thread_ts": "123"},
            {"user": "carol", "text": "msg3", "timestamp": "125", "thread_ts": "123"},
        ]
        threads = count_threaded_discussions(messages)
        self.assertEqual(threads, 2)

    def test_save_and_load_channel_config(self):
        config = {"channels": ["general", "engineering"], "last_updated": "2026-06-23"}
        save_channel_config(config)
        loaded = load_channel_config()
        self.assertEqual(loaded, config)

    def test_build_slack_context_handles_no_token(self):
        context = build_slack_context()
        self.assertIn("not configured", context.lower())

    @patch("slack_connector.get_slack_client")
    def test_build_slack_context_with_mock_client(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.conversations_list.return_value = {"channels": [{"id": "C123", "name": "general"}]}
        mock_client.conversations_history.return_value = {"messages": [
            {"text": "We decided to deploy", "user": "U123", "ts": "1234", "thread_ts": None, "bot_id": None}
        ]}

        config = {"channels": ["general"]}
        save_channel_config(config)

        context = build_slack_context(monitored_channels=["general"])
        self.assertIn("slack team context", context.lower())


if __name__ == "__main__":
    unittest.main()
