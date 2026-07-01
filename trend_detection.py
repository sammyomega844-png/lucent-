import json
from datetime import date, timedelta
from pathlib import Path
from statistics import mean, stdev


def _load_snapshot(day):
    """Load snapshot for a specific date."""
    path = Path(f"snapshot_{day.isoformat()}.json")
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _extract_metrics(snapshot):
    """Extract comparable metrics from a snapshot."""
    if not snapshot:
        return None

    tasks = snapshot.get("tasks", {})
    inventory = snapshot.get("inventory", {})
    crm = snapshot.get("crm", {})

    completed = sum(1 for t in tasks.values() if t.get("status") == "Completed")
    high_open = sum(1 for t in tasks.values() if t.get("priority") == "High" and t.get("status") != "Completed")
    overdue = sum(1 for t in tasks.values() if t.get("status") != "Completed" and t.get("due_date", "") < str(date.today()))
    stock_alerts = sum(1 for i in inventory.values() if int(i.get("stock", 0)) < int(i.get("reorder", 0)))
    qualified_leads = sum(1 for c in crm.values() if c.get("status") == "Qualified")
    pipeline_value = sum(float(c.get("value", 0)) for c in crm.values() if c.get("status") != "Lost")
    lost_deals = sum(1 for c in crm.values() if c.get("status") == "Lost")

    return {
        "date": snapshot.get("date", str(date.today())),
        "completed_tasks": completed,
        "high_priority_open": high_open,
        "overdue_tasks": overdue,
        "stock_alerts": stock_alerts,
        "qualified_leads": qualified_leads,
        "pipeline_value": pipeline_value,
        "lost_deals": lost_deals,
    }


def load_historical_metrics(days_back=14):
    """Load metrics for past N days."""
    today = date.today()
    metrics = []
    for offset in range(days_back, -1, -1):
        day = today - timedelta(days=offset)
        snapshot = _load_snapshot(day)
        if snapshot:
            m = _extract_metrics(snapshot)
            if m:
                metrics.append(m)
    return metrics


def calculate_trends(metrics):
    """Calculate trend direction and velocity for each metric."""
    if len(metrics) < 2:
        return {}

    trends = {}
    keys = ["completed_tasks", "high_priority_open", "overdue_tasks", "stock_alerts", "qualified_leads", "pipeline_value", "lost_deals"]

    for key in keys:
        values = [m.get(key, 0) for m in metrics]
        if len(values) < 2:
            continue

        recent = values[-3:] if len(values) >= 3 else values
        older = values[:-3] if len(values) >= 3 else []

        if older:
            older_avg = mean(older)
            recent_avg = mean(recent)
            direction = "up" if recent_avg > older_avg else "down" if recent_avg < older_avg else "flat"
            velocity = abs(recent_avg - older_avg) / max(abs(older_avg), 0.1)
        else:
            direction = "flat"
            velocity = 0.0

        if len(values) >= 2:
            change_pct = ((values[-1] - values[-2]) / max(abs(values[-2]), 0.1)) * 100 if values[-2] != 0 else 0.0
        else:
            change_pct = 0.0

        trends[key] = {
            "direction": direction,
            "velocity": round(velocity, 2),
            "change_pct": round(change_pct, 1),
            "latest": values[-1] if values else 0,
        }

    return trends


def detect_anomalies(metrics, threshold_sigma=2.0):
    """Detect sudden changes or anomalies in recent data."""
    if len(metrics) < 3:
        return []

    anomalies = []
    keys = ["completed_tasks", "high_priority_open", "overdue_tasks", "stock_alerts", "qualified_leads", "pipeline_value", "lost_deals"]

    for key in keys:
        values = [m.get(key, 0) for m in metrics[-7:]]
        if len(values) < 3:
            continue

        try:
            avg = mean(values)
            std = stdev(values) if len(values) > 1 else 0
            if std == 0:
                continue

            latest = values[-1]
            z_score = abs((latest - avg) / std)
            if z_score > threshold_sigma:
                direction = "spike" if latest > avg else "drop"
                anomalies.append({"metric": key, "direction": direction, "z_score": round(z_score, 2), "value": latest})
        except Exception:
            continue

    return anomalies


def build_trend_context():
    """Build a human-readable trend summary for the briefing prompt."""
    metrics = load_historical_metrics(days_back=14)
    if len(metrics) < 2:
        return "Insufficient historical data for trend analysis yet."

    trends = calculate_trends(metrics)
    anomalies = detect_anomalies(metrics)

    lines = ["TREND ANALYSIS (Past 14 days):"]

    for key, trend_data in trends.items():
        if trend_data["direction"] != "flat":
            arrow = "📈" if trend_data["direction"] == "up" else "📉"
            lines.append(f"  {arrow} {key.replace('_', ' ').title()}: {trend_data['direction']} ({trend_data['change_pct']:+.0f}% vs yesterday)")

    if anomalies:
        lines.append("ANOMALIES DETECTED:")
        for anom in anomalies[:3]:
            icon = "⚠️" if anom["direction"] == "spike" else "🔴"
            lines.append(f"  {icon} {anom['metric'].replace('_', ' ').title()}: significant {anom['direction']} (z-score: {anom['z_score']})")

    return "\n".join(lines)


if __name__ == "__main__":
    context = build_trend_context()
    print(context)
