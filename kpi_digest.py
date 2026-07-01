"""
KPI Performance Digest — tracks KPI trends across snapshots,
computes momentum (improving / stable / declining), and flags
regressions before they become problems.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REPORT_FILE = "kpi_digest_report.json"


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _load_snapshot(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None


def _snapshot_metrics(snapshot):
    tasks = snapshot.get("tasks", {})
    inventory = snapshot.get("inventory", {})
    crm = snapshot.get("crm", {})

    completed = 0
    high_open = 0
    overdue = 0
    for task in tasks.values():
        status = str(task.get("status", "")).strip()
        if status == "Completed":
            completed += 1
        elif status != "Completed":
            if task.get("priority") == "High":
                high_open += 1
            due = task.get("due_date") or task.get("Due_Date") or task.get("due") or ""
            if due:
                try:
                    from datetime import date
                    due_date = date.fromisoformat(str(due)[:10])
                    if due_date < date.today():
                        overdue += 1
                except Exception:
                    pass

    stock_alerts = 0
    for item in inventory.values():
        try:
            if int(item.get("stock", 0)) < int(item.get("reorder", 0)):
                stock_alerts += 1
        except Exception:
            continue

    qualified = 0
    pipeline_value = 0.0
    lost = 0
    for lead in crm.values():
        status = str(lead.get("status", "")).strip()
        if status == "Qualified":
            qualified += 1
        elif status == "Lost":
            lost += 1
        if status != "Lost":
            try:
                pipeline_value += float(lead.get("value", 0))
            except Exception:
                pass

    return {
        "completed_tasks": completed,
        "high_priority_open": high_open,
        "overdue_tasks": overdue,
        "stock_alerts": stock_alerts,
        "qualified_leads": qualified,
        "pipeline_value": round(pipeline_value, 2),
        "lost_deals": lost,
    }


def _trend(values):
    """Return 'improving', 'stable', or 'declining' from a list of values (oldest first)."""
    if len(values) < 2:
        return "stable"
    half = len(values) // 2
    first_half_avg = sum(values[:half]) / half
    second_half_avg = sum(values[half:]) / (len(values) - half)
    delta = second_half_avg - first_half_avg
    if abs(delta) < 0.5:
        return "stable"
    return "improving" if delta < 0 else "declining"  # fewer = better for most KPIs


def _pipeline_trend(values):
    """For pipeline value, more is better."""
    if len(values) < 2:
        return "stable"
    half = len(values) // 2
    first_half_avg = sum(values[:half]) / half
    second_half_avg = sum(values[half:]) / (len(values) - half)
    delta = second_half_avg - first_half_avg
    if abs(delta) < 100:
        return "stable"
    return "improving" if delta > 0 else "declining"


def build_kpi_digest(snapshot_dir=".", days=14):
    from datetime import date, timedelta
    today = date.today()
    rows = []

    for offset in range(days - 1, -1, -1):
        day = today - timedelta(days=offset)
        snapshot_path = Path(snapshot_dir) / f"snapshot_{day.isoformat()}.json"
        if not snapshot_path.exists():
            continue
        snapshot = _load_snapshot(snapshot_path)
        if not snapshot:
            continue
        metrics = _snapshot_metrics(snapshot)
        metrics["date"] = day.isoformat()
        rows.append(metrics)

    if not rows:
        return {
            "generated_at": _now_iso(),
            "summary": "KPI digest: no snapshot data found.",
            "kpis": {},
            "rows": [],
            "flags": [],
        }

    kpi_keys = ["completed_tasks", "high_priority_open", "overdue_tasks",
                "stock_alerts", "qualified_leads", "pipeline_value", "lost_deals"]

    kpis = {}
    flags = []
    for key in kpi_keys:
        values = [r[key] for r in rows]
        latest = values[-1]
        avg = sum(values) / len(values)
        trend_fn = _pipeline_trend if key == "pipeline_value" else _trend
        trend = trend_fn(values)
        kpis[key] = {"latest": latest, "avg": round(avg, 1), "trend": trend}
        if trend == "declining":
            flags.append(f"{key.replace('_', ' ')} is declining (latest {latest}, avg {avg:.1f})")

    # Summary sentence
    declining_count = sum(1 for v in kpis.values() if v["trend"] == "declining")
    improving_count = sum(1 for v in kpis.values() if v["trend"] == "improving")
    summary_bits = [f"KPI digest: {len(rows)} day(s) of data"]
    if improving_count:
        summary_bits.append(f"{improving_count} KPI(s) improving")
    if declining_count:
        summary_bits.append(f"{declining_count} KPI(s) declining — review flags")
    if not declining_count and not improving_count:
        summary_bits.append("all KPIs stable")

    # Latest values
    latest_row = rows[-1]
    summary_bits.append(
        f"pipeline ${latest_row['pipeline_value']:,.0f}, "
        f"{latest_row['qualified_leads']} qualified, "
        f"{latest_row['overdue_tasks']} overdue task(s)"
    )

    return {
        "generated_at": _now_iso(),
        "summary": "; ".join(summary_bits) + ".",
        "kpis": kpis,
        "rows": rows,
        "flags": flags,
    }


def write_kpi_digest(path=DEFAULT_REPORT_FILE, snapshot_dir=".", days=14):
    data = build_kpi_digest(snapshot_dir=snapshot_dir, days=days)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_kpi_digest(path=DEFAULT_REPORT_FILE):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "summary": "No KPI digest yet.", "kpis": {}, "rows": [], "flags": []}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "summary": "No KPI digest yet.", "kpis": {}, "rows": [], "flags": []}
