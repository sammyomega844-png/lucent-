import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_REPORT_FILE = "pipeline_risk_report.json"


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=240):
    text = str(value or "").strip()
    return text[:max_len]


def _parse_date(value):
    text = _safe_text(value, max_len=40)
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except Exception:
            continue
    return None


def _normalize_haystack(value):
    return re.sub(r"\s+", " ", _safe_text(value, max_len=1000).lower())


def _status_base_score(status):
    normalized = str(status or "").strip().lower()
    if normalized == "qualified":
        return 64
    if normalized == "contacted":
        return 52
    if normalized == "new":
        return 42
    return 46


def _value_bonus(lead_value):
    try:
        value = float(lead_value)
    except Exception:
        return 0
    if value <= 0:
        return 0
    return min(int(math.log10(value + 1) * 5), 15)


def _staleness_adjustment(last_contact, created_at):
    contact_date = _parse_date(last_contact) or _parse_date(created_at)
    if not contact_date:
        return 12, "no contact date"

    days_since = (datetime.now(timezone.utc).date() - contact_date).days
    if days_since <= 3:
        return -10, f"touched {days_since} day(s) ago"
    if days_since <= 7:
        return -4, f"touched {days_since} day(s) ago"
    if days_since <= 14:
        return 4, f"touched {days_since} day(s) ago"
    if days_since <= 30:
        return 12, f"touched {days_since} day(s) ago"
    return 20, f"touched {days_since} day(s) ago"


def _collect_related_signals(company, lead_name, open_sources):
    matches = []
    company_key = _normalize_haystack(company)
    lead_key = _normalize_haystack(lead_name)

    for source_name, items in open_sources:
        for item in items:
            text = " ".join(
                _safe_text(item.get(field, ""), max_len=220)
                for field in ("title", "owner", "reason", "next_step", "nudge_subject", "nudge_body")
            ).lower()
            if company_key and company_key in text:
                matches.append((source_name, text))
                continue
            if lead_key and lead_key in text:
                matches.append((source_name, text))

    return matches


def build_pipeline_risk_report(crm_df, action_register=None, follow_up_plan=None, meeting_execution_plan=None, max_items=10):
    if crm_df is None or getattr(crm_df, "empty", True):
        return {
            "generated_at": _now_iso(),
            "summary": "Pipeline risk: no CRM rows found.",
            "counts": {"total": 0, "risk": 0, "watch": 0, "stable": 0, "closed_lost": 0},
            "items": [],
        }

    open_sources = [
        ("action_register", (action_register or {}).get("items", [])),
        ("follow_up", (follow_up_plan or {}).get("items", [])),
        ("meeting_execution", (meeting_execution_plan or {}).get("items", [])),
    ]

    items = []
    closed_lost = 0
    for _, row in crm_df.iterrows():
        status = _safe_text(row.get("Status", ""), max_len=40)
        if status.strip().lower() == "lost":
            closed_lost += 1
            continue

        company = _safe_text(row.get("Company", "Unknown company"), max_len=160)
        lead_name = _safe_text(row.get("Lead_Name", "Unknown lead"), max_len=160)
        lead_value = row.get("Lead_Value", 0)
        created_at = row.get("Created_At", "")
        last_contact = row.get("Last_Contact", "")

        base_score = _status_base_score(status)
        value_bonus = _value_bonus(lead_value)
        staleness_adjustment, staleness_reason = _staleness_adjustment(last_contact, created_at)
        related_signals = _collect_related_signals(company, lead_name, open_sources)
        related_bonus = min(len(related_signals) * 6, 18)

        score = max(min(base_score + value_bonus + staleness_adjustment + related_bonus, 100), 0)
        if score >= 70:
            bucket = "risk"
        elif score >= 45:
            bucket = "watch"
        else:
            bucket = "stable"

        items.append({
            "source": "crm",
            "company": company,
            "lead_name": lead_name,
            "status": status,
            "lead_value": float(lead_value) if str(lead_value).strip() else 0,
            "score": score,
            "bucket": bucket,
            "reason": ", ".join([
                status or "unknown status",
                staleness_reason,
                f"{len(related_signals)} related open item(s)",
            ]),
            "next_step": (
                "Escalate now and reset the close plan." if bucket == "risk" else
                "Reconnect and confirm the next milestone." if bucket == "watch" else
                "Keep cadence and protect momentum."
            ),
            "related_open_items": len(related_signals),
        })

    items.sort(key=lambda item: item.get("score", 0), reverse=True)
    items = items[:max_items]

    counts = {
        "total": len(items),
        "risk": sum(1 for item in items if item.get("bucket") == "risk"),
        "watch": sum(1 for item in items if item.get("bucket") == "watch"),
        "stable": sum(1 for item in items if item.get("bucket") == "stable"),
        "closed_lost": closed_lost,
    }

    top_risk = next((item for item in items if item.get("bucket") == "risk"), None)
    top_value = next((item for item in items if item.get("lead_value", 0) > 0), None)

    if counts["total"] == 0:
        summary = "Pipeline risk radar: no active opportunities found."
    else:
        summary_bits = [
            f"Pipeline risk radar: {counts['total']} active deal(s) scored",
            f"{counts['risk']} at risk",
            f"{counts['watch']} watch",
            f"{counts['stable']} stable",
        ]
        if top_risk:
            summary_bits.append(f"top risk {top_risk['company']} ({top_risk['score']}/100)")
        if top_value:
            summary_bits.append(f"highest value {top_value['company']} (${top_value['lead_value']:,.0f})")
        summary = "; ".join(summary_bits) + "."

    return {
        "generated_at": _now_iso(),
        "summary": summary,
        "counts": counts,
        "items": items,
    }


def write_pipeline_risk_report(path=DEFAULT_REPORT_FILE, **kwargs):
    data = build_pipeline_risk_report(**kwargs)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_pipeline_risk_report(path=DEFAULT_REPORT_FILE):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "summary": "No pipeline risk report yet.", "counts": {}, "items": []}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "summary": "No pipeline risk report yet.", "counts": {}, "items": []}