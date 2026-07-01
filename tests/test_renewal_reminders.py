import unittest
from pathlib import Path
import tempfile
import pandas as pd
from datetime import date, timedelta

from renewal_reminders import build_renewal_reminders, load_renewal_reminders, write_renewal_reminders


class RenewalRemindersTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os; os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os; os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_overdue_renewal_flagged(self):
        overdue_date = (date.today() - timedelta(days=10)).isoformat()
        crm = pd.DataFrame([
            {"Lead_Name": "John", "Company": "TechInc", "Status": "Qualified",
             "Lead_Value": 5000, "Last_Contact": "", "Renewal_Date": overdue_date},
        ])
        report = build_renewal_reminders(crm)
        self.assertEqual(report["counts"]["overdue"], 1)
        self.assertIn("overdue", report["summary"].lower())

    def test_upcoming_renewal_flagged(self):
        upcoming_date = (date.today() + timedelta(days=20)).isoformat()
        crm = pd.DataFrame([
            {"Lead_Name": "Sara", "Company": "WebSoft", "Status": "Contacted",
             "Lead_Value": 2500, "Last_Contact": "", "Renewal_Date": upcoming_date},
        ])
        report = build_renewal_reminders(crm)
        self.assertEqual(report["counts"]["this_month"], 1)

    def test_lost_excluded(self):
        upcoming_date = (date.today() + timedelta(days=10)).isoformat()
        crm = pd.DataFrame([
            {"Lead_Name": "Mike", "Company": "Lost Co", "Status": "Lost",
             "Lead_Value": 0, "Last_Contact": "", "Renewal_Date": upcoming_date},
        ])
        report = build_renewal_reminders(crm)
        self.assertEqual(report["counts"]["total"], 0)

    def test_no_renewal_fields_uses_proxy(self):
        # No Renewal_Date field — should use last_contact + 365 as proxy
        crm = pd.DataFrame([
            {"Lead_Name": "Sam", "Company": "ProxyCo", "Status": "Qualified",
             "Lead_Value": 1000, "Last_Contact": (date.today() - timedelta(days=300)).isoformat()},
        ])
        report = build_renewal_reminders(crm)
        # 365 - 300 = 65 days until renewal — within 90-day window
        self.assertGreaterEqual(report["counts"]["total"], 1)

    def test_write_and_load(self):
        crm = pd.DataFrame([
            {"Lead_Name": "John", "Company": "TechInc", "Status": "Qualified",
             "Lead_Value": 5000, "Last_Contact": "2026-01-01",
             "Renewal_Date": (date.today() + timedelta(days=15)).isoformat()},
        ])
        path = write_renewal_reminders(crm_df=crm)
        self.assertTrue(Path(path).exists())
        loaded = load_renewal_reminders()
        self.assertIn("items", loaded)


if __name__ == "__main__":
    unittest.main()
