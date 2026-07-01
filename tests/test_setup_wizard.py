import tempfile
import unittest
from pathlib import Path

from setup_wizard import build_setup_summary, render_setup_wizard_html, write_setup_wizard


class SetupWizardTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_setup_summary_returns_dict(self):
        summary = build_setup_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn("readiness_score", summary)

    def test_render_setup_wizard_html_contains_title(self):
        html = render_setup_wizard_html()
        self.assertIn("Client onboarding made obvious", html)

    def test_write_setup_wizard_creates_files(self):
        html_path, json_path = write_setup_wizard()
        self.assertTrue(Path(html_path).exists())
        self.assertTrue(Path(json_path).exists())


if __name__ == "__main__":
    unittest.main()
