import tempfile
import unittest
from pathlib import Path

from meeting_pipeline import build_meeting_execution_plan, load_meeting_execution_plan, write_meeting_execution_plan


class MeetingPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_meeting_execution_plan_uses_notes_and_sources(self):
        meeting_notes = """
Meeting: Weekly ops sync
- Ship the dashboard by Friday, owner: Mia, due: 2026-06-28
- Confirm supplier call, owner: Omar
"""
        action_register = {
            "items": [
                {"source": "email", "title": "Urgent invoice review", "owner": "Client Team", "score": 40, "reason": "email from client"}
            ]
        }
        follow_up_plan = {
            "items": [
                {"source": "task_followup", "title": "Call supplier", "owner": "Mia", "score": 70, "reason": "overdue by 4 days"}
            ]
        }

        plan = build_meeting_execution_plan(meeting_notes=meeting_notes, action_register=action_register, follow_up_plan=follow_up_plan)

        self.assertGreaterEqual(plan["counts"]["total"], 2)
        self.assertEqual(plan["counts"]["meeting_notes"], 2)
        self.assertIn("Meeting-to-execution", plan["summary"])
        self.assertTrue(any(item["source"] == "meeting_notes" for item in plan["items"]))

    def test_write_and_load_meeting_execution_plan(self):
        path = write_meeting_execution_plan(meeting_notes="Meeting: Weekly ops sync\n- Confirm supplier call, owner: Omar")
        self.assertTrue(Path(path).exists())

        loaded = load_meeting_execution_plan()
        self.assertIn("summary", loaded)
        self.assertIn("items", loaded)


if __name__ == "__main__":
    unittest.main()