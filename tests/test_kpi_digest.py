import tempfile
import unittest
from pathlib import Path

from kpi_digest import build_kpi_digest, load_kpi_digest, write_kpi_digest


class KpiDigestTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_kpi_digest_no_snapshots(self):
        report = build_kpi_digest()
        self.assertIn("summary", report)
        self.assertIn("kpis", report)
        self.assertIn("rows", report)
        self.assertIn("flags", report)
        self.assertEqual(report["rows"], [])

    def test_build_kpi_digest_with_snapshot(self):
        import json
        from datetime import date
        today = date.today().isoformat()
        snapshot = {
            "tasks": {
                "1": {"status": "Completed", "priority": "High"},
                "2": {"status": "In Progress", "priority": "High", "Due_Date": "2020-01-01"},
            },
            "inventory": {
                "A": {"stock": "5", "reorder": "10"},
            },
            "crm": {
                "L1": {"status": "Qualified", "value": "5000"},
                "L2": {"status": "Lost", "value": "0"},
            },
        }
        Path(f"snapshot_{today}.json").write_text(json.dumps(snapshot), encoding="utf-8")

        report = build_kpi_digest()
        self.assertEqual(len(report["rows"]), 1)
        self.assertIn("pipeline_value", report["kpis"])
        self.assertIn("KPI digest", report["summary"])

    def test_write_and_load_kpi_digest(self):
        path = write_kpi_digest()
        self.assertTrue(Path(path).exists())
        loaded = load_kpi_digest()
        self.assertIn("summary", loaded)


if __name__ == "__main__":
    unittest.main()
