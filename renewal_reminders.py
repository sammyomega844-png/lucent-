"""
Renewal Reminders — surfaces upcoming contract end dates, renewal
windows, and customer milestones from CRM data.
Falls back gracefully when no renewal fields are present.
No paid APIs. Fully offline.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REPORT_FILE = "renewal_reminders.json"

# Column names to look for renewal/contract dates in the CRM
_RENEWAL_FIELDS = [
    "Renewal_Date", "renewal_date", "Contract_End", "contract_end",
    "Expiry_Date", "expiry_date", "Next_Review", "next_review",
]

# Look ahead this many days for upcoming renewals
_LOOKAHEAD_DAYS = 90


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=160):
    return str(value or "").strip()[:max_len]


def _parse_date(value):
    text = _safe_text(value, max_len=40)
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except Exception:
            continue
    return None


def _find_renewal_date(row):
    """Check all known renewal field names and return the first valid date found."""
    for field in _RENEWAL_FIELDS:
        val = row.get(field, "")
        if val and str(val).strip():
            parsed = _parse_date(str(val).strip())
            if parsed:
                return parsed, field
    return None, None


def build_renewal_reminders(crm_df, lookahead_days=_LOOKAHEAD_DAYS):
    if crm_df is None or getattr(crm_df, "empty", True):
        return {
            "generated_at": _now_iso(),
            "summary": "Renewal reminders: no CRM data.",
            "counts": {"total": 0, "overdue": 0, "this_month": 0, "upcoming": 0},
            "items": [],
        }

    from datetime import date, timedelta
    today = date.today()
    horizon = today + timedelta(days=lookahead_days)

    items = []
    no_renewal_field = 0

    for _, row in crm_df.iterrows():
        status = _safe_text(row.get("Status", "")).lower()
        if status == "lost":
            continue

        company = _safe_text(row.get("Company", "Unknown"))
        lead_name = _safe_text(row.get("Lead_Name", ""))
        lead_value = float(row.get("Lead_Value", 0) or 0)
        last_contact = _safe_text(row.get("Last_Contact", ""), max_len=40)

        renewal_date, renewal_field = _find_renewal_date(row)

        if renewal_date is None:
            # Use last_contact + 365 as a synthetic "annual renewal" proxy
            lc = _parse_date(last_contact)
            if lc:
                from datetime import timedelta as td
                renewal_date = lc + td(days=365)
                renewal_field = "estimated (last contact + 1yr)"
            else:
                no_renewal_field += 1
                continue

        days_until = (renewal_date - today).days

        if days_until < 0:
            urgency = "overdue"
            label = f"Overdue by {abs(days_until)}d"
        elif days_until <= 30:
            urgency = "this_month"
            label = f"Due in {days_until}d"
        elif days_until <= lookahead_days:
            urgency = "upcoming"
            label = f"Due in {days_until}d"
        else:
            continue  # outside lookahead window

        if urgency == "overdue":
            next_step = "Renewal is overdue — reach out immediately to avoid lapse."
        elif urgency == "this_month":
            next_step = f"Renewal due within 30 days — confirm intent and prepare paperwork."
        else:
            next_step = f"Renewal coming up in ~{days_until} days — schedule a touchpoint."

        items.append({
            "company": company,
            "lead_name": lead_name,
            "status": _safe_text(row.get("Status", "")),
            "lead_value": lead_value,
            "renewal_date": renewal_date.isoformat(),
            "renewal_field": renewal_field,
            "days_until": days_until,
            "urgency": urgency,
            "label": label,
            "next_step": next_step,
            "last_contact": last_contact,
        })

    items.sort(key=lambda x: x["days_until"])

    counts = {
        "total": len(items),
        "overdue": sum(1 for i in items if i["urgency"] == "overdue"),
        "this_month": sum(1 for i in items if i["urgency"] == "this_month"),
        "upcoming": sum(1 for i in items if i["urgency"] == "upcoming"),
    }

    if not items:
        summary = f"Renewal reminders: no renewals due in the next {lookahead_days} days."
    else:
        summary_bits = [
            f"Renewal reminders: {counts['total']} due in next {lookahead_days}d",
            f"{counts['overdue']} overdue",
            f"{counts['this_month']} this month",
            f"{counts['upcoming']} upcoming",
        ]
        if items:
            top = items[0]
            summary_bits.append(f"next: {top['company']} ({top['label']})")
        summary = "; ".join(summary_bits) + "."

    return {
        "generated_at": _now_iso(),
        "summary": summary,
        "counts": counts,
        "items": items,
        "lookahead_days": lookahead_days,
    }


def write_renewal_reminders(path=DEFAULT_REPORT_FILE, **kwargs):
    data = build_renewal_reminders(**kwargs)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_renewal_reminders(path=DEFAULT_REPORT_FILE):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "summary": "No renewal reminders yet.", "counts": {}, "items": []}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "summary": "No renewal reminders yet.", "counts": {}, "items": []}
