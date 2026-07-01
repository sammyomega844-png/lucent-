import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from quick_response import (
    approve_draft,
    create_approval_drafts,
    list_pending_drafts,
    load_draft_queue,
    send_approved_drafts,
    summarize_queue,
)


class QuickResponseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    @staticmethod
    def _emails():
        return [
            {
                "sender": "Client Team <client@example.com>",
                "subject": "Urgent: contract review needed",
                "snippet": "Please review by tomorrow",
                "body": "Can you confirm by 10am tomorrow?",
            },
            {
                "sender": "newsletter@example.com",
                "subject": "Weekly newsletter",
                "snippet": "Top stories",
                "body": "Not actionable",
            },
        ]

    def test_create_approval_drafts_filters_actionable(self):
        queue = create_approval_drafts(
            self._emails(),
            ai_generate=lambda _: "Draft response body.",
            max_drafts=5,
        )

        self.assertEqual(len(queue.get("drafts", [])), 1)
        self.assertEqual(queue["drafts"][0]["status"], "needs_approval")
        self.assertEqual(queue["drafts"][0]["to"], "client@example.com")

    def test_approve_draft_updates_status(self):
        queue = create_approval_drafts(self._emails(), ai_generate=lambda _: "Draft body")
        draft_id = queue["drafts"][0]["id"]

        approved = approve_draft(draft_id, approved_by="manager")
        self.assertTrue(approved)

        updated = load_draft_queue()
        self.assertEqual(updated["drafts"][0]["status"], "approved")
        self.assertEqual(updated["drafts"][0]["approved_by"], "manager")

    @patch("quick_response.smtplib.SMTP")
    def test_send_approved_drafts_marks_sent(self, mock_smtp):
        queue = create_approval_drafts(self._emails(), ai_generate=lambda _: "Draft body")
        draft_id = queue["drafts"][0]["id"]
        approve_draft(draft_id)

        result = send_approved_drafts(
            smtp_host="smtp.gmail.com",
            smtp_port=587,
            smtp_username="sender@example.com",
            smtp_password="pass",
            from_email="sender@example.com",
        )

        self.assertEqual(result["sent"], 1)
        self.assertEqual(result["failed"], 0)

        updated = load_draft_queue()
        self.assertEqual(updated["drafts"][0]["status"], "sent")
        mock_smtp.assert_called_once()

    def test_queue_summary_and_pending_list(self):
        queue = create_approval_drafts(self._emails(), ai_generate=lambda _: "Draft body")
        text = summarize_queue(queue)
        self.assertIn("pending_approval=1", text)

        pending = list_pending_drafts()
        self.assertEqual(len(pending), 1)

    def test_audit_file_written(self):
        create_approval_drafts(self._emails(), ai_generate=lambda _: "Draft body")
        audit = Path("response_audit_log.jsonl")
        self.assertTrue(audit.exists())

        line = audit.read_text(encoding="utf-8").splitlines()[0]
        payload = json.loads(line)
        self.assertEqual(payload["event"], "draft_created")


if __name__ == "__main__":
    unittest.main()
