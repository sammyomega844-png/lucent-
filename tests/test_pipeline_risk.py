import tempfile
import unittest
from pathlib import Path

import pandas as pd

from pipeline_risk import build_pipeline_risk_report, load_pipeline_risk_report, write_pipeline_risk_report


class PipelineRiskTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_pipeline_risk_report_scores_active_deals(self):
        crm = pd.DataFrame([
            {"Lead_Name": "John Doe", "Company": "TechInc", "Status": "Qualified", "Lead_Value": 5000, "Created_At": "2026-06-01", "Last_Contact": "2026-06-01"},
            {"Lead_Name": "Sara Smith", "Company": "WebSoft", "Status": "Contacted", "Lead_Value": 2500, "Created_At": "2026-05-01", "Last_Contact": "2026-05-10"},
            {"Lead_Name": "Mike Ross", "Company": "Ross Law", "Status": "Lost", "Lead_Value": 0, "Created_At": "2026-04-01", "Last_Contact": "2026-04-15"},
        ])
        action_register = {"items": [{"title": "TechInc close plan", "owner": "John Doe", "reason": "approval pending"}]}
        follow_up_plan = {"items": [{"title": "WebSoft follow-up", "owner": "Sara Smith", "reason": "stale deal"}]}
        meeting_execution_plan = {"items": [{"title": "TechInc decision", "owner": "John Doe", "reason": "next step"}]}

        report = build_pipeline_risk_report(
            crm,
            action_register=action_register,
            follow_up_plan=follow_up_plan,
            meeting_execution_plan=meeting_execution_plan,
        )

        self.assertEqual(report["counts"]["closed_lost"], 1)
        self.assertEqual(report["counts"]["total"], 2)
        self.assertIn("Pipeline risk radar", report["summary"])
        self.assertTrue(any(item["bucket"] in {"risk", "watch", "stable"} for item in report["items"]))

    def test_write_and_load_pipeline_risk_report(self):
        crm = pd.DataFrame([
            {"Lead_Name": "John Doe", "Company": "TechInc", "Status": "Qualified", "Lead_Value": 5000, "Created_At": "2026-06-01", "Last_Contact": "2026-06-01"},
        ])
        path = write_pipeline_risk_report(
            crm_df=crm,
            action_register={"items": []},
            follow_up_plan={"items": []},
            meeting_execution_plan={"items": []},
        )
        self.assertTrue(Path(path).exists())

        loaded = load_pipeline_risk_report()
        self.assertIn("summary", loaded)
        self.assertIn("items", loaded)


if __name__ == "__main__":
    unittest.main()