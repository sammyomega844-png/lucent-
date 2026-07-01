import tempfile
import unittest
from pathlib import Path

from design_system import build_design_system_css, write_design_system_css
from design_system_preview import build_design_system_preview_html, write_design_system_preview


class DesignSystemTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_build_design_system_css_has_tokens(self):
        css = build_design_system_css()
        self.assertIn("--ds-brand", css)
        self.assertIn(".ds-btn.primary", css)

    def test_write_design_system_css_creates_file(self):
        path = write_design_system_css()
        self.assertTrue(Path(path).exists())

    def test_build_design_system_preview_html_contains_title(self):
        html = build_design_system_preview_html()
        self.assertIn("Design System Preview", html)
        self.assertIn("Lucent Design System", html)

    def test_write_design_system_preview_creates_file(self):
        path = write_design_system_preview()
        self.assertTrue(Path(path).exists())


if __name__ == "__main__":
    unittest.main()
