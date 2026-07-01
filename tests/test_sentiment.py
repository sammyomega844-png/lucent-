import unittest

from sentiment import build_sentiment_report, flag_emails


class SentimentTests(unittest.TestCase):
    def test_urgent_email_flagged(self):
        emails = [{"subject": "URGENT action required", "from": "boss@company.com", "body": "Please respond asap.", "date": "2026-06-24"}]
        report = build_sentiment_report(emails)
        self.assertEqual(report["counts"]["urgent"], 1)
        self.assertIn("urgent", report["summary"].lower())

    def test_routine_email_flagged(self):
        emails = [{"subject": "Newsletter June 2026", "from": "noreply@news.com", "body": "Unsubscribe here.", "date": "2026-06-24"}]
        report = build_sentiment_report(emails)
        self.assertGreaterEqual(report["counts"]["routine"], 1)

    def test_empty_list(self):
        report = build_sentiment_report([])
        self.assertEqual(report["counts"]["total"], 0)
        self.assertIn("no emails", report["summary"].lower())

    def test_flag_emails_sorted_by_score(self):
        emails = [
            {"subject": "hi", "from": "a@b.com", "body": "", "date": ""},
            {"subject": "URGENT: critical issue", "from": "c@d.com", "body": "immediately respond", "date": ""},
        ]
        flagged = flag_emails(emails)
        self.assertGreater(flagged[0]["score"], flagged[1]["score"])


if __name__ == "__main__":
    unittest.main()
