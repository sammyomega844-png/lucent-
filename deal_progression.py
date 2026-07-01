"""
Deal Progression Timeline — measures how long each CRM deal has spent
in its current stage, flags deals stuck longer than the cohort average,
and produces a ranked list of deals needing a stage push.
No paid APIs. Fully offline.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REPORT_FILE = "deal_progression.json"

# Expected max days in each stage before a deal is considered stuck
_STAGE_THRESHOLDS = {
    "new": 7,
    "contacted": 14,
    "qualified": 30,
}


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=160):
    return str(value or "").strip()[:max_len]


def _parse_date(value):
    text = _safe_text(value, max_len=40)
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except Exception:
            continue
    return None


def build_deal_progression(crm_df):
    if crm_df is None or getattr(crm_df, "empty", True):
        return {
            "generated_at": _now_iso(),
            "summary": "Deal progression: no CRM data.",
            "counts": {"total": 0, "stuck": 0, "on_track": 0, "closed_lost": 0},
            "items": [],
        }

    from datetime import date
    today = date.today()
    items = []
    closed_lost = 0

    for _, row in crm_df.iterrows():
        status = _safe_text(row.get("Status", "")).lower()
        if status == "lost":
            closed_lost += 1
            continue

        company = _safe_text(row.get("Company", "Unknown"))
        lead_name = _safe_text(row.get("Lead_Name", ""))
        lead_value = float(row.get("Lead_Value", 0) or 0)

        created = _parse_date(row.get("Created_At", ""))
        last = _parse_date(row.get("Last_Contact", ""))

        age_days = (today - created).days if created else 0
        days_since_contact = (today - last).days if last else age_days

        threshold = _STAGE_THRESHOLDS.get(status, 21)
        stuck = days_since_contact > threshold

        if stuck:
            stage_label = "stuck"
            next_step = f"Push out of '{status}' — last touched {days_since_contact}d ago, threshold is {threshold}d."
        else:
            stage_label = "on_track"
            next_step = f"On track — {threshold - days_since_contact}d remaining before stage threshold."

        items.append({
            "company": company,
            "lead_name": lead_name,
            "status": _safe_text(row.get("Status", "")),
            "lead_value": lead_value,
            "age_days": age_days,
            "days_since_contact": days_since_contact,
            "stage_threshold_days": threshold,
            "stage_label": stage_label,
            "next_step": next_step,
        })

    # Sort: stuck first, then by days_since_contact descending
    items.sort(key=lambda x: (x["stage_label"] != "stuck", -x["days_since_contact"]))

    stuck_count = sum(1 for i in items if i["stage_label"] == "stuck")
    on_track_count = sum(1 for i in items if i["stage_label"] == "on_track")

    if not items:
        summary = "Deal progression: no active deals."
    else:
        summary_bits = [
            f"Deal progression: {len(items)} active deal(s)",
            f"{stuck_count} stuck",
            f"{on_track_count} on track",
        ]
        if stuck_count > 0:
            top = next(i for i in items if i["stage_label"] == "stuck")
            summary_bits.append(f"oldest stuck: {top['company']} ({top['days_since_contact']}d in '{top['status']}')")
        summary = "; ".join(summary_bits) + "."

    return {
        "generated_at": _now_iso(),
        "summary": summary,
        "counts": {
            "total": len(items),
            "stuck": stuck_count,
            "on_track": on_track_count,
            "closed_lost": closed_lost,
        },
        "items": items,
    }


def write_deal_progression(path=DEFAULT_REPORT_FILE, **kwargs):
    data = build_deal_progression(**kwargs)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_deal_progression(path=DEFAULT_REPORT_FILE):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "summary": "No deal progression data yet.", "counts": {}, "items": []}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "summary": "No deal progression data yet.", "counts": {}, "items": []}
