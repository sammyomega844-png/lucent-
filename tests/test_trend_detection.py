import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
import json

from trend_detection import calculate_trends, detect_anomalies, load_historical_metrics, build_trend_context


class TrendDetectionTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        import os
        os.chdir(str(self.old_cwd))
        self.temp_dir.cleanup()

    def test_calculate_trends_shows_direction(self):
        metrics = [
            {"date": "2026-06-10", "completed_tasks": 2, "qualified_leads": 5},
            {"date": "2026-06-11", "completed_tasks": 4, "qualified_leads": 8},
            {"date": "2026-06-12", "completed_tasks": 8, "qualified_leads": 15},
            {"date": "2026-06-13", "completed_tasks": 12, "qualified_leads": 20},
        ]
        trends = calculate_trends(metrics)
        self.assertEqual(trends.get("completed_tasks", {}).get("direction"), "up")

    def test_detect_anomalies_flags_outliers(self):
        metrics = [
            {"date": f"2026-06-{10+i:02d}", "completed_tasks": 5, "stock_alerts": 2}
            for i in range(7)
        ]
        metrics.append({"date": "2026-06-17", "completed_tasks": 25, "stock_alerts": 2})
        anomalies = detect_anomalies(metrics, threshold_sigma=1.5)
        self.assertTrue(any(a["metric"] == "completed_tasks" for a in anomalies))

    def test_load_historical_metrics_empty_when_no_files(self):
        metrics = load_historical_metrics(days_back=7)
        self.assertEqual(metrics, [])

    def test_build_trend_context_returns_string(self):
        context = build_trend_context()
        self.assertIsInstance(context, str)
        self.assertTrue("Insufficient" in context or "TREND" in context)


if __name__ == "__main__":
    unittest.main()
