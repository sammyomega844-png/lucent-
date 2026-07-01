import tempfile
import unittest
from pathlib import Path

from landing_page import build_landing_page_html, write_landing_page


class LandingPageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_landing_page_html_returns_string(self):
        html = build_landing_page_html()
        self.assertIsInstance(html, str)
        self.assertIn("Lucent", html)
        self.assertNotIn("View roadmap", html)

    def test_write_landing_page_creates_file(self):
        path = write_landing_page()
        self.assertTrue(Path(path).exists())


if __name__ == "__main__":
    unittest.main()
