import tempfile
import unittest
from pathlib import Path

from dashboard import write_dashboard, build_dashboard_html


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_dashboard_html_returns_string(self):
        html = build_dashboard_html()
        self.assertIsInstance(html, str)
        self.assertIn("Lucent", html)
        self.assertNotIn("Open status tracker", html)
        self.assertIn("Action register", html)
        self.assertIn("Pipeline risk radar", html)
        self.assertIn("Approval workflow", html)
        self.assertIn("Recommendations", html)
        self.assertIn("KPI digest", html)
        self.assertIn("Communication timeline", html)
        self.assertIn("Product tour", html)
        self.assertIn("Revenue forecast", html)
        self.assertIn("Deal progression", html)
        self.assertIn("Renewal reminders", html)

    def test_write_dashboard_creates_file(self):
        path = write_dashboard()
        self.assertTrue(Path(path).exists())


if __name__ == "__main__":
    unittest.main()
