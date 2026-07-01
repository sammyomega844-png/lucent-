import os
import tempfile
import unittest
from pathlib import Path

from premium_report import render_premium_report, write_premium_report


class PremiumReportTests(unittest.TestCase):
    def test_render_contains_scores_and_feedback_links(self):
        html = render_premium_report(
            today="Monday, 23 June 2026",
            loaded_at="08:05 AM",
            overall_score=82,
            day_rating="Good",
            market_signal_score=61,
            market_signal_label="Market strength",
            news_context="News context: profile=industry=real estate",
            roadmap_summary="Priority focus and milestones",
            briefing="Top priorities for today",
            one_click_feedback_links=[("property market", "http://127.0.0.1:8001/vote?topic=property")],
        )
        self.assertIn("Executive Morning Briefing", html)
        self.assertIn("Day Score: 82/100", html)
        self.assertIn("Upvote property market", html)

    def test_write_creates_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.html"
            path = write_premium_report(
                output,
                today="Monday, 23 June 2026",
                loaded_at="08:05 AM",
                overall_score=78,
                day_rating="Needs Attention",
                market_signal_score=49,
                market_signal_label="Market mixed",
                news_context="News context: general business coverage.",
                roadmap_summary="Roadmap",
                briefing="Briefing",
                one_click_feedback_links=[],
            )
            self.assertTrue(Path(path).exists())
            self.assertIn("Executive Morning Briefing", Path(path).read_text(encoding="utf-8"))

    def test_render_shows_weekly_digest_hint_or_link(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            old_cwd = Path.cwd()
            try:
                temp_path = Path(temp_dir)
                # No digest file: should show hint text.
                os.chdir(temp_path)
                no_file_html = render_premium_report(
                    today="Monday, 23 June 2026",
                    loaded_at="08:05 AM",
                    overall_score=78,
                    day_rating="Needs Attention",
                    market_signal_score=49,
                    market_signal_label="Market mixed",
                    news_context="News context: general business coverage.",
                    roadmap_summary="Roadmap",
                    briefing="Briefing",
                    one_click_feedback_links=[],
                )
                self.assertIn("Weekly digest not generated yet", no_file_html)

                # Digest exists: should show file link.
                Path("weekly_digest.html").write_text("<html></html>", encoding="utf-8")
                with_file_html = render_premium_report(
                    today="Monday, 23 June 2026",
                    loaded_at="08:05 AM",
                    overall_score=78,
                    day_rating="Needs Attention",
                    market_signal_score=49,
                    market_signal_label="Market mixed",
                    news_context="News context: general business coverage.",
                    roadmap_summary="Roadmap",
                    briefing="Briefing",
                    one_click_feedback_links=[],
                )
                self.assertIn("Open weekly_digest.html", with_file_html)
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
