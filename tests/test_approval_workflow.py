import tempfile
import unittest
from pathlib import Path

from approval_workflow import build_approval_workflow_report, load_approval_workflow_report, write_approval_workflow_report


class ApprovalWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_approval_workflow_report_empty_queue(self):
        report = build_approval_workflow_report()

        self.assertIn("summary", report)
        self.assertIn("counts", report)
        self.assertIn("items", report)
        self.assertEqual(report["counts"].get("total_pending", 0), 0)

    def test_write_and_load_approval_workflow_report(self):
        path = write_approval_workflow_report()
        self.assertTrue(Path(path).exists())

        loaded = load_approval_workflow_report()
        self.assertIn("summary", loaded)
        self.assertIn("counts", loaded)
        self.assertIn("items", loaded)

    def test_approve_draft_in_workflow(self):
        from approval_workflow import approve_draft_in_workflow, reject_draft_in_workflow
        
        # Create a mock queue file with a draft
        import json
        queue = {
            "drafts": [
                {
                    "id": "d-123",
                    "recipient": "test@example.com",
                    "subject": "Test",
                    "body": "Test body",
                    "status": "needs_approval",
                    "created_at": "2026-06-24T00:00:00+00:00",
                }
            ]
        }
        Path("response_drafts.json").write_text(json.dumps(queue), encoding="utf-8")

        # Approve it
        result = approve_draft_in_workflow("d-123", queue_path="response_drafts.json")
        self.assertTrue(result)

        # Verify status changed
        updated_queue = json.loads(Path("response_drafts.json").read_text(encoding="utf-8"))
        self.assertEqual(updated_queue["drafts"][0]["status"], "approved")

    def test_reject_draft_in_workflow(self):
        from approval_workflow import reject_draft_in_workflow
        
        import json
        queue = {
            "drafts": [
                {
                    "id": "d-456",
                    "recipient": "test@example.com",
                    "subject": "Test",
                    "body": "Test body",
                    "status": "needs_approval",
                    "created_at": "2026-06-24T00:00:00+00:00",
                }
            ]
        }
        Path("response_drafts.json").write_text(json.dumps(queue), encoding="utf-8")

        result = reject_draft_in_workflow("d-456", reason="needs revision", queue_path="response_drafts.json")
        self.assertTrue(result)

        updated_queue = json.loads(Path("response_drafts.json").read_text(encoding="utf-8"))
        self.assertEqual(updated_queue["drafts"][0]["status"], "rejected")
        self.assertEqual(updated_queue["drafts"][0]["rejection_reason"], "needs revision")


if __name__ == "__main__":
    unittest.main()
