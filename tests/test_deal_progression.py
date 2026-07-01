import unittest
from pathlib import Path
import tempfile
import pandas as pd

from deal_progression import build_deal_progression, load_deal_progression, write_deal_progression


class DealProgressionTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os; os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os; os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def _crm(self):
        return pd.DataFrame([
            {"Lead_Name": "John Doe", "Company": "TechInc", "Status": "Qualified",
             "Lead_Value": 5000, "Created_At": "2026-06-01", "Last_Contact": "2026-06-23"},
            {"Lead_Name": "Sara Smith", "Company": "WebSoft", "Status": "Contacted",
             "Lead_Value": 2500, "Created_At": "2026-04-01", "Last_Contact": "2026-04-15"},
            {"Lead_Name": "Mike Ross", "Company": "Ross Law", "Status": "Lost",
             "Lead_Value": 0, "Created_At": "2026-03-01", "Last_Contact": "2026-03-15"},
        ])

    def test_lost_excluded_from_items(self):
        report = build_deal_progression(self._crm())
        companies = [i["company"] for i in report["items"]]
        self.assertNotIn("Ross Law", companies)
        self.assertEqual(report["counts"]["closed_lost"], 1)

    def test_stale_deal_flagged_stuck(self):
        report = build_deal_progression(self._crm())
        websoft = next((i for i in report["items"] if i["company"] == "WebSoft"), None)
        self.assertIsNotNone(websoft)
        self.assertEqual(websoft["stage_label"], "stuck")

    def test_summary_contains_progression(self):
        report = build_deal_progression(self._crm())
        self.assertIn("Deal progression", report["summary"])

    def test_write_and_load(self):
        path = write_deal_progression(crm_df=self._crm())
        self.assertTrue(Path(path).exists())
        loaded = load_deal_progression()
        self.assertIn("items", loaded)


if __name__ == "__main__":
    unittest.main()
