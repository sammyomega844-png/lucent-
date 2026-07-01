import tempfile
import unittest
from pathlib import Path

import pandas as pd

from communication_timeline import build_communication_timeline, load_communication_timeline, write_communication_timeline


class CommunicationTimelineTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def _crm(self):
        return pd.DataFrame([
            {"Lead_Name": "John Doe", "Company": "TechInc", "Status": "Qualified", "Lead_Value": 5000, "Last_Contact": "2026-06-20"},
            {"Lead_Name": "Sara Smith", "Company": "WebSoft", "Status": "Contacted", "Lead_Value": 2500, "Last_Contact": "2026-06-01"},
        ])

    def test_build_communication_timeline_basic(self):
        report = build_communication_timeline(self._crm())
        self.assertIn("summary", report)
        self.assertIn("accounts", report)
        self.assertIn("TechInc", report["accounts"])
        self.assertIn("WebSoft", report["accounts"])

    def test_email_matches_company(self):
        emails = [{"subject": "TechInc proposal", "from": "john@techinc.com", "body": "Hi", "date": "2026-06-21"}]
        report = build_communication_timeline(self._crm(), emails=emails)
        techinc = report["accounts"]["TechInc"]
        sources = [t["source"] for t in techinc["touches"]]
        self.assertIn("email", sources)

    def test_write_and_load(self):
        path = write_communication_timeline(crm_df=self._crm())
        self.assertTrue(Path(path).exists())
        loaded = load_communication_timeline()
        self.assertIn("accounts", loaded)


if __name__ == "__main__":
    unittest.main()
