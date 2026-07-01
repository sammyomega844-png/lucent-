import tempfile
import unittest
from pathlib import Path

import pandas as pd

from action_register import build_action_register, load_action_register, write_action_register


class ActionRegisterTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_action_register_merges_sources(self):
        tasks = pd.DataFrame([
            {"Task_Name": "Call supplier", "Status": "Pending", "Priority": "High", "Assignee": "Mia", "Due_Date": "2026-06-24"},
            {"Task_Name": "Fix typo", "Status": "Completed", "Priority": "Low", "Assignee": "Mia", "Due_Date": "2026-06-20"},
        ])
        emails = [
            {"sender": "Client Team <client@example.com>", "subject": "Urgent: invoice review needed", "snippet": "Please review", "body": "Need approval today."},
            {"sender": "newsletter@example.com", "subject": "Weekly newsletter", "snippet": "Read now", "body": "No action."},
        ]
        slack_context = """
SLACK TEAM CONTEXT (Last 24 hours):

  📌 #general:
    Action items: 1 found
      • Please update the proposal by Friday
    Decisions made: 1 found
      ✓ We decided to launch next week
"""
        quick_response_queue = {
            "drafts": [
                {"status": "needs_approval", "reply_subject": "Re: urgent invoice review", "original_sender": "Client Team <client@example.com>", "to": "client@example.com"}
            ]
        }

        register = build_action_register(tasks, emails=emails, slack_context=slack_context, quick_response_queue=quick_response_queue)

        self.assertGreaterEqual(register["counts"]["total"], 3)
        self.assertEqual(register["counts"]["reply_drafts"], 1)
        self.assertTrue(register["items"][0]["score"] >= register["items"][-1]["score"])

    def test_write_and_load_action_register(self):
        tasks = pd.DataFrame([
            {"Task_Name": "Call supplier", "Status": "Pending", "Priority": "High", "Assignee": "Mia", "Due_Date": "2026-06-24"},
        ])
        path = write_action_register(tasks_df=tasks, emails=[], slack_context="")
        self.assertTrue(Path(path).exists())

        loaded = load_action_register()
        self.assertIn("summary", loaded)
        self.assertIn("items", loaded)


if __name__ == "__main__":
    unittest.main()