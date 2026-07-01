import os
import tempfile
import unittest
from pathlib import Path

from status_sync import STATUS_END, STATUS_START, update_project_status


class StatusSyncTests(unittest.TestCase):
    def test_updates_existing_marker_block(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "project_status.html"
            file_path.write_text(
                "<html><body>\n"
                f"{STATUS_START}\nold\n{STATUS_END}\n"
                "</body></html>",
                encoding="utf-8",
            )

            ok = update_project_status(path=file_path, source="unit-test")
            self.assertTrue(ok)
            text = file_path.read_text(encoding="utf-8")
            self.assertIn("Source: unit-test", text)

    def test_inserts_marker_before_tabs_if_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "project_status.html"
            file_path.write_text(
                "<html><body>\n<p class=\"subtitle\">x</p>\n<div class=\"tabs\">\n</div>\n</body></html>",
                encoding="utf-8",
            )

            ok = update_project_status(path=file_path, source="unit-test")
            self.assertTrue(ok)
            text = file_path.read_text(encoding="utf-8")
            self.assertIn(STATUS_START, text)
            self.assertIn("Source: unit-test", text)

    def test_missing_file_returns_false(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "does_not_exist.html"
            ok = update_project_status(path=file_path, source="unit-test")
            self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
