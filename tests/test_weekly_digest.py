import json
import os
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from weekly_digest import build_weekly_digest, write_weekly_digest


class WeeklyDigestTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)

        for day_offset in [0, 1, 2]:
            day = date.today() - timedelta(days=day_offset)
            path = Path(f"snapshot_{day.isoformat()}.json")
            payload = {
                "tasks": {
                    "1": {"status": "Completed", "priority": "High", "completion": 1.0},
                    "2": {"status": "In Progress", "priority": "High", "completion": 0.4},
                },
                "inventory": {
                    "A1": {"stock": 5, "reorder": 10, "discontinued": False},
                },
                "crm": {
                    "L1": {"status": "Qualified", "value": 12000},
                    "L2": {"status": "Contacted", "value": 8000},
                },
            }
            path.write_text(json.dumps(payload), encoding="utf-8")

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.temp_dir.cleanup()

    def test_build_weekly_digest_has_rows_and_summary(self):
        digest = build_weekly_digest(days=7)
        self.assertGreaterEqual(len(digest["days"]), 3)
        self.assertIn("avg_completed", digest["summary"])
        self.assertIn("avg_pipeline_value", digest["summary"])

    def test_write_weekly_digest_outputs_files(self):
        html_path, json_path = write_weekly_digest(days=7)
        self.assertTrue(Path(html_path).exists())
        self.assertTrue(Path(json_path).exists())


if __name__ == "__main__":
    unittest.main()
