"""
Customer Communication Timeline — aggregates all recorded touches
with a customer (emails, tasks, Slack mentions, CRM notes) into a
single ordered history per account.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REPORT_FILE = "communication_timeline.json"


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=240):
    return str(value or "").strip()[:max_len]


def _normalize(text):
    return re.sub(r"\s+", " ", _safe_text(text, max_len=1000).lower())


def _matches(text, company, lead_name):
    haystack = _normalize(text)
    if company and _normalize(company) in haystack:
        return True
    if lead_name and _normalize(lead_name) in haystack:
        return True
    return False


def _touch_sort_key(touch):
    return touch.get("date", "")


def build_communication_timeline(crm_df, emails=None, tasks_df=None, slack_messages=None, max_touches=8):
    """
    Build a per-account communication timeline from all available data sources.
    Returns a dict keyed by company name with ordered touch history.
    """
    if crm_df is None or getattr(crm_df, "empty", True):
        return {
            "generated_at": _now_iso(),
            "summary": "Communication timeline: no CRM rows found.",
            "accounts": {},
        }

    accounts = {}
    for _, row in crm_df.iterrows():
        company = _safe_text(row.get("Company", "Unknown"), max_len=160)
        lead_name = _safe_text(row.get("Lead_Name", ""), max_len=160)
        last_contact = _safe_text(row.get("Last_Contact", ""), max_len=40)
        status = _safe_text(row.get("Status", ""), max_len=40)
        lead_value = row.get("Lead_Value", 0)

        touches = []

        # CRM entry itself as the anchor touch
        if last_contact:
            touches.append({
                "source": "crm",
                "date": last_contact,
                "summary": f"CRM record — status: {status}, value: ${lead_value}",
                "type": "crm",
            })

        # Emails
        for email in (emails or []):
            subject = _safe_text(email.get("subject", ""), max_len=120)
            sender = _safe_text(email.get("from", ""), max_len=120)
            body = _safe_text(email.get("body", ""), max_len=400)
            date_str = _safe_text(email.get("date", ""), max_len=40)
            if _matches(subject + " " + sender + " " + body, company, lead_name):
                touches.append({
                    "source": "email",
                    "date": date_str[:10] if date_str else "",
                    "summary": f"Email: {subject[:80]} (from {sender[:40]})",
                    "type": "email",
                })

        # Tasks
        if tasks_df is not None:
            for _, task in tasks_df.iterrows():
                task_name = _safe_text(task.get("Task_Name", ""), max_len=180)
                assignee = _safe_text(task.get("Assignee", ""), max_len=80)
                due = _safe_text(task.get("Due_Date", ""), max_len=40)
                notes = _safe_text(task.get("Notes", ""), max_len=200)
                if _matches(task_name + " " + assignee + " " + notes, company, lead_name):
                    touches.append({
                        "source": "task",
                        "date": due[:10] if due else "",
                        "summary": f"Task: {task_name[:80]} — {assignee}",
                        "type": "task",
                    })

        # Slack
        for msg in (slack_messages or []):
            text = _safe_text(msg.get("text", ""), max_len=400)
            ts = _safe_text(msg.get("date", msg.get("timestamp", "")), max_len=40)
            user = _safe_text(msg.get("user", ""), max_len=80)
            if _matches(text, company, lead_name):
                touches.append({
                    "source": "slack",
                    "date": ts[:10] if ts else "",
                    "summary": f"Slack: {text[:80]} ({user})",
                    "type": "slack",
                })

        touches.sort(key=_touch_sort_key, reverse=True)
        touches = touches[:max_touches]

        accounts[company] = {
            "lead_name": lead_name,
            "status": status,
            "lead_value": float(lead_value) if str(lead_value).strip() else 0.0,
            "last_contact": last_contact,
            "touch_count": len(touches),
            "touches": touches,
        }

    active = {k: v for k, v in accounts.items() if v["status"].lower() != "lost"}
    total_touches = sum(v["touch_count"] for v in accounts.values())
    summary_bits = [
        f"Communication timeline: {len(accounts)} account(s)",
        f"{len(active)} active",
        f"{total_touches} total touches recorded",
    ]

    return {
        "generated_at": _now_iso(),
        "summary": "; ".join(summary_bits) + ".",
        "accounts": accounts,
    }


def write_communication_timeline(path=DEFAULT_REPORT_FILE, **kwargs):
    data = build_communication_timeline(**kwargs)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_communication_timeline(path=DEFAULT_REPORT_FILE):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "summary": "No communication timeline yet.", "accounts": {}}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "summary": "No communication timeline yet.", "accounts": {}}
