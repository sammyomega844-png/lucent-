import os
import tempfile
import unittest

from news_connector import build_news_topics, capture_news_feedback, get_news_context_summary, normalize_feedback_topics, record_news_feedback, record_quick_feedback, reset_news_preferences


class NewsPreferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        reset_news_preferences()

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.temp_dir.cleanup()

    def test_feedback_terms_are_added_to_topics(self):
        record_news_feedback(["property market", "mortgage rates"], source="unit-test")
        topics = build_news_topics()
        self.assertIn("property market", topics)
        self.assertIn("mortgage rates", topics)

    def test_news_context_summary_includes_profile_and_feedback(self):
        os.environ["USER_INDUSTRY"] = "real estate"
        os.environ["USER_REGION"] = "Dubai"
        os.environ["USER_INTERESTS"] = "mortgage rates"
        record_news_feedback(["property market"], source="unit-test")

        summary = get_news_context_summary()

        self.assertIn("real estate", summary.lower())
        self.assertIn("dubai", summary.lower())
        self.assertIn("property market", summary.lower())

    def test_capture_news_feedback_records_topics(self):
        saved = capture_news_feedback(["infrastructure", "supply chain"], source="unit-test")

        self.assertIn("infrastructure", saved.get("topics", {}))
        self.assertIn("supply chain", saved.get("topics", {}))

    def test_normalize_feedback_topics_splits_and_dedupes(self):
        topics = normalize_feedback_topics(["Property Market", " mortgage rates ", "property market", "construction"])

        self.assertEqual(topics, ["property market", "mortgage rates", "construction"])

    def test_record_quick_feedback_persists_topics(self):
        saved = record_quick_feedback("thumbs_up", topics=["construction", "mortgage rates"], source="unit-test")

        self.assertIn("construction", saved.get("topics", {}))
        self.assertIn("mortgage rates", saved.get("topics", {}))


if __name__ == "__main__":
    unittest.main()
