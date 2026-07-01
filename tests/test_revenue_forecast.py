import unittest
from pathlib import Path
import tempfile
import pandas as pd

from revenue_forecast import build_revenue_forecast, load_revenue_forecast, write_revenue_forecast


class RevenueForecastTests(unittest.TestCase):
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
             "Lead_Value": 5000, "Created_At": "2026-05-01", "Last_Contact": "2026-06-01"},
            {"Lead_Name": "Sara Smith", "Company": "WebSoft", "Status": "Contacted",
             "Lead_Value": 2500, "Created_At": "2026-04-01", "Last_Contact": "2026-05-01"},
            {"Lead_Name": "Mike Ross", "Company": "Ross Law", "Status": "Lost",
             "Lead_Value": 0, "Created_At": "2026-03-01", "Last_Contact": "2026-03-15"},
        ])

    def test_build_excludes_lost(self):
        report = build_revenue_forecast(self._crm())
        companies = [d["company"] for d in report["active_deals"]]
        self.assertNotIn("Ross Law", companies)
        self.assertEqual(len(report["active_deals"]), 2)

    def test_horizons_present(self):
        report = build_revenue_forecast(self._crm())
        self.assertIn("30", report["horizons"])
        self.assertIn("60", report["horizons"])
        self.assertIn("90", report["horizons"])

    def test_summary_contains_forecast(self):
        report = build_revenue_forecast(self._crm())
        self.assertIn("Revenue forecast", report["summary"])

    def test_empty_crm(self):
        report = build_revenue_forecast(pd.DataFrame())
        self.assertIn("no CRM data", report["summary"])

    def test_write_and_load(self):
        path = write_revenue_forecast(crm_df=self._crm())
        self.assertTrue(Path(path).exists())
        loaded = load_revenue_forecast()
        self.assertIn("horizons", loaded)


if __name__ == "__main__":
    unittest.main()
