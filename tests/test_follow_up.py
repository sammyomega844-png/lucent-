import tempfile
import unittest
from pathlib import Path

import pandas as pd

from follow_up import build_follow_up_plan, load_follow_up_plan, write_follow_up_plan


class FollowUpTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_follow_up_plan_flags_overdue_and_drafts(self):
        tasks = pd.DataFrame([
            {"Task_Name": "Call supplier", "Status": "Pending", "Priority": "High", "Assignee": "Mia", "Due_Date": "2026-06-20"},
            {"Task_Name": "Future task", "Status": "In Progress", "Priority": "Medium", "Assignee": "Mia", "Due_Date": "2099-01-01"},
        ])
        action_register = {
            "items": [
                {"source": "email", "title": "Urgent invoice review", "owner": "Client Team", "score": 40, "reason": "email from client"},
            ]
        }
        quick_response_queue = {
            "drafts": [
                {"status": "needs_approval", "reply_subject": "Re: urgent invoice review", "original_sender": "Client Team <client@example.com>", "to": "client@example.com"}
            ]
        }

        plan = build_follow_up_plan(tasks, action_register=action_register, quick_response_queue=quick_response_queue)

        self.assertGreaterEqual(plan["counts"]["total"], 2)
        self.assertEqual(plan["counts"]["reply_drafts"], 1)
        self.assertIn("Follow-up autopilot", plan["summary"])
        self.assertTrue(any(item["source"] == "reply_draft" for item in plan["items"]))

    def test_write_and_load_follow_up_plan(self):
        tasks = pd.DataFrame([
            {"Task_Name": "Call supplier", "Status": "Pending", "Priority": "High", "Assignee": "Mia", "Due_Date": "2026-06-20"},
        ])
        path = write_follow_up_plan(tasks_df=tasks, action_register={"items": []}, quick_response_queue={"drafts": []})
        self.assertTrue(Path(path).exists())

        loaded = load_follow_up_plan()
        self.assertIn("summary", loaded)
        self.assertIn("items", loaded)


if __name__ == "__main__":
    unittest.main()