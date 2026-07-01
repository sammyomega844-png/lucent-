import tempfile
import unittest
from pathlib import Path

import pandas as pd

from customer_health import build_customer_health_report, load_customer_health_report, write_customer_health_report


class CustomerHealthTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_customer_health_report_scores_crm_rows(self):
        crm = pd.DataFrame([
            {"Lead_Name": "John Doe", "Company": "TechInc", "Status": "Qualified", "Lead_Value": 5000, "Last_Contact": "2026-06-23"},
            {"Lead_Name": "Sara Smith", "Company": "WebSoft", "Status": "Contacted", "Lead_Value": 2500, "Last_Contact": "2026-06-05"},
            {"Lead_Name": "Mike Ross", "Company": "Ross Law", "Status": "Lost", "Lead_Value": 0, "Last_Contact": "2026-05-01"},
        ])
        action_register = {"items": [{"title": "TechInc contract review", "owner": "John Doe", "score": 50, "reason": "email from client"}]}
        follow_up_plan = {"items": [{"title": "Follow up: TechInc renewal", "owner": "John Doe", "score": 80, "reason": "overdue by 2 days"}]}
        meeting_execution_plan = {"items": [{"title": "TechInc next step", "owner": "John Doe", "score": 70, "reason": "meeting note", "next_step": "confirm deadline"}]}

        report = build_customer_health_report(
            crm,
            action_register=action_register,
            follow_up_plan=follow_up_plan,
            meeting_execution_plan=meeting_execution_plan,
        )

        self.assertEqual(report["counts"]["total"], 3)
        self.assertIn("Customer health radar", report["summary"])
        self.assertTrue(any(item["bucket"] in {"healthy", "watch", "risk"} for item in report["items"]))

    def test_write_and_load_customer_health_report(self):
        crm = pd.DataFrame([
            {"Lead_Name": "John Doe", "Company": "TechInc", "Status": "Qualified", "Lead_Value": 5000, "Last_Contact": "2026-06-23"},
        ])
        path = write_customer_health_report(crm_df=crm, action_register={"items": []}, follow_up_plan={"items": []}, meeting_execution_plan={"items": []})
        self.assertTrue(Path(path).exists())

        loaded = load_customer_health_report()
        self.assertIn("summary", loaded)
        self.assertIn("items", loaded)


if __name__ == "__main__":
    unittest.main()