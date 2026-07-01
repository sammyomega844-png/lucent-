import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_REPORT_FILE = "customer_health_report.json"


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


def _status_base_score(status):
    normalized = str(status or "").strip().lower()
    if normalized == "qualified":
        return 82
    if normalized == "contacted":
        return 68
    if normalized == "lost":
        return 35
    return 55


def _value_bonus(lead_value):
    try:
        value = float(lead_value)
    except Exception:
        return 0
    if value <= 0:
        return 0
    return min(int(math.log10(value + 1) * 4), 12)


def _recency_adjustment(last_contact):
    contact_date = _parse_date(last_contact)
    if not contact_date:
        return -5, "no recent contact date"

    days_since = (datetime.now(timezone.utc).date() - contact_date).days
    if days_since <= 7:
        return 10, f"contacted {days_since} day(s) ago"
    if days_since <= 14:
        return 4, f"contacted {days_since} day(s) ago"
    if days_since <= 30:
        return -4, f"contacted {days_since} day(s) ago"
    return -12, f"contacted {days_since} day(s) ago"


def _normalize_haystack(value):
    return re.sub(r"\s+", " ", _safe_text(value, max_len=1000).lower())


def _collect_related_signals(company, lead_name, open_sources):
    haystacks = []
    company_key = _normalize_haystack(company)
    lead_key = _normalize_haystack(lead_name)

    for source_name, items in open_sources:
        for item in items:
            text = " ".join(
                _safe_text(item.get(field, ""), max_len=220)
                for field in ("title", "owner", "reason", "next_step", "nudge_subject", "nudge_body")
            ).lower()
            if company_key and company_key in text:
                haystacks.append((source_name, text))
                continue
            if lead_key and lead_key in text:
                haystacks.append((source_name, text))

    return haystacks


def build_customer_health_report(crm_df, action_register=None, follow_up_plan=None, meeting_execution_plan=None, max_items=10):
    if crm_df is None or getattr(crm_df, "empty", True):
        return {
            "generated_at": _now_iso(),
            "summary": "Customer health: no CRM rows found.",
            "counts": {"total": 0, "healthy": 0, "watch": 0, "risk": 0},
            "items": [],
        }

    open_sources = [
        ("action_register", (action_register or {}).get("items", [])),
        ("follow_up", (follow_up_plan or {}).get("items", [])),
        ("meeting_execution", (meeting_execution_plan or {}).get("items", [])),
    ]

    items = []
    for _, row in crm_df.iterrows():
        company = _safe_text(row.get("Company", "Unknown company"), max_len=160)
        lead_name = _safe_text(row.get("Lead_Name", "Unknown lead"), max_len=160)
        status = _safe_text(row.get("Status", ""), max_len=40)
        lead_value = row.get("Lead_Value", 0)
        base_score = _status_base_score(status)
        value_bonus = _value_bonus(lead_value)
        recency_adjustment, recency_reason = _recency_adjustment(row.get("Last_Contact", ""))
        related_signals = _collect_related_signals(company, lead_name, open_sources)
        related_penalty = min(len(related_signals) * 6, 18)

        score = max(min(base_score + value_bonus + recency_adjustment - related_penalty, 100), 0)
        if score >= 75:
            bucket = "healthy"
        elif score >= 50:
            bucket = "watch"
        else:
            bucket = "risk"

        items.append({
            "source": "crm",
            "company": company,
            "lead_name": lead_name,
            "status": status,
            "lead_value": float(lead_value) if str(lead_value).strip() else 0,
            "score": score,
            "bucket": bucket,
            "reason": ", ".join([status or "unknown status", recency_reason, f"{len(related_signals)} related open item(s)"] ),
            "next_step": (
                "Keep cadence and expand the account." if bucket == "healthy" else
                "Send a follow-up and confirm next milestone." if bucket == "watch" else
                "Escalate and re-engage before the lead stalls."
            ),
            "related_open_items": len(related_signals),
        })

    items.sort(key=lambda item: item.get("score", 0), reverse=True)
    items = items[:max_items]

    counts = {
        "total": len(items),
        "healthy": sum(1 for item in items if item.get("bucket") == "healthy"),
        "watch": sum(1 for item in items if item.get("bucket") == "watch"),
        "risk": sum(1 for item in items if item.get("bucket") == "risk"),
    }

    top_risk = next((item for item in reversed(items) if item.get("bucket") == "risk"), None)
    top_opportunity = next((item for item in items if item.get("bucket") == "healthy"), None)

    summary_bits = [
        f"Customer health radar: {counts['total']} lead(s) scored",
        f"{counts['healthy']} healthy",
        f"{counts['watch']} watch",
        f"{counts['risk']} at risk",
    ]
    if top_risk:
        summary_bits.append(f"top risk {top_risk['company']} ({top_risk['score']}/100)")
    if top_opportunity:
        summary_bits.append(f"top opportunity {top_opportunity['company']} ({top_opportunity['score']}/100)")

    return {
        "generated_at": _now_iso(),
        "summary": "; ".join(summary_bits) + ".",
        "counts": counts,
        "items": items,
    }


def write_customer_health_report(path=DEFAULT_REPORT_FILE, **kwargs):
    data = build_customer_health_report(**kwargs)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_customer_health_report(path=DEFAULT_REPORT_FILE):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "summary": "No customer health report yet.", "counts": {}, "items": []}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "summary": "No customer health report yet.", "counts": {}, "items": []}
