import unittest

from recommendations import build_recommendations


class RecommendationsTests(unittest.TestCase):
    def test_empty_signals_no_crash(self):
        report = build_recommendations()
        self.assertIn("summary", report)
        self.assertIn("items", report)
        self.assertIn("counts", report)

    def test_risk_account_generates_rec(self):
        ch = {"items": [{"company": "TechInc", "lead_name": "John", "bucket": "risk", "score": 40, "reason": "stale"}]}
        report = build_recommendations(customer_health_report=ch)
        titles = [r["title"] for r in report["items"]]
        self.assertTrue(any("TechInc" in t for t in titles))

    def test_high_score_action_register_item_generates_rec(self):
        ar = {"items": [{"title": "Contract review", "owner": "Jane", "score": 85, "reason": "email from client"}]}
        report = build_recommendations(action_register=ar)
        self.assertGreater(report["counts"]["total"], 0)
        high_recs = [r for r in report["items"] if r["priority"] == "high"]
        self.assertTrue(len(high_recs) > 0)

    def test_priority_ordering(self):
        ar = {"items": [{"title": "Urgent task", "owner": "Sam", "score": 90, "reason": "email"}]}
        fu = {"items": [{"title": "Draft", "reason": "approval needed", "owner": "Sam"}]}
        report = build_recommendations(action_register=ar, follow_up_plan=fu)
        items = report["items"]
        if len(items) >= 2:
            priority_order = {"high": 0, "medium": 1, "low": 2}
            for i in range(len(items) - 1):
                self.assertLessEqual(
                    priority_order.get(items[i]["priority"], 2),
                    priority_order.get(items[i + 1]["priority"], 2),
                )


if __name__ == "__main__":
    unittest.main()
