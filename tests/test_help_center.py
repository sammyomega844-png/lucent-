import tempfile
import unittest
from pathlib import Path

from help_center import build_help_center_html, write_help_center


class HelpCenterTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_help_center_html_is_string(self):
        content = build_help_center_html()
        self.assertIsInstance(content, str)
        self.assertIn("Lucent", content)
        self.assertIn("Help Center", content)

    def test_all_features_present(self):
        content = build_help_center_html()
        for feature_id in ["daily-briefing", "action-register", "approval-workflow",
                           "customer-health", "pipeline-risk", "recommendations",
                           "kpi-digest", "communication-timeline", "email-sentiment"]:
            self.assertIn(feature_id, content)

    def test_write_help_center_creates_file(self):
        path = write_help_center()
        self.assertTrue(Path(path).exists())
        content = Path(path).read_text(encoding="utf-8")
        self.assertIn("Help Center", content)


if __name__ == "__main__":
    unittest.main()
