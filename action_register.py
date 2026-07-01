import json
import re
from datetime import datetime, timedelta, timezone
from email.utils import parseaddr
from pathlib import Path


ACTION_KEYWORDS = [
    "urgent",
    "asap",
    "follow up",
    "follow-up",
    "deadline",
    "approval",
    "review",
    "proposal",
    "invoice",
    "issue",
    "support",
    "request",
    "blocked",
    "needs",
    "please",
]


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=280):
    text = str(value or "").strip()
    return text[:max_len]


def _extract_email(sender):
    _, email = parseaddr(str(sender or ""))
    if email and "@" in email:
        return email
    return ""


def _dedupe_items(items):
    seen = set()
    output = []
    for item in items:
        key = (item.get("title", "") or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def _task_priority_score(row):
    score = 0
    status = str(row.get("Status", "")).strip().lower()
    priority = str(row.get("Priority", "")).strip().lower()
    due_date = str(row.get("Due_Date", "")).strip()

    if status not in {"completed", "done"}:
        score += 20
    if priority == "high":
        score += 30
    elif priority == "medium":
        score += 15

    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        delta = due.date() - datetime.now(timezone.utc).date()
        if delta < timedelta(days=0):
            score += 40
        elif delta <= timedelta(days=2):
            score += 25
        elif delta <= timedelta(days=5):
            score += 10
    except Exception:
        pass

    return score


def extract_task_actions(tasks_df, max_items=5):
    items = []
    if tasks_df is None or getattr(tasks_df, "empty", True):
        return items

    for _, row in tasks_df.iterrows():
        status = str(row.get("Status", "")).strip().lower()
        if status in {"completed", "done"}:
            continue

        title = _safe_text(row.get("Task_Name", "Untitled task"), max_len=180)
        owner = _safe_text(row.get("Assignee", "Unassigned"), max_len=80)
        due_date = _safe_text(row.get("Due_Date", ""), max_len=40)
        priority = _safe_text(row.get("Priority", ""), max_len=20)
        score = _task_priority_score(row)
        reason_bits = []
        if priority.lower() == "high":
            reason_bits.append("high priority")
        if due_date:
            reason_bits.append(f"due {due_date}")
        if status:
            reason_bits.append(status)

        items.append({
            "source": "task",
            "title": title,
            "owner": owner,
            "due_date": due_date,
            "priority": priority,
            "score": score,
            "reason": ", ".join(reason_bits) or "needs attention",
        })

    items.sort(key=lambda item: item.get("score", 0), reverse=True)
    return items[:max_items]


def _email_action_score(email_obj):
    subject = _safe_text(email_obj.get("subject", "")).lower()
    snippet = _safe_text(email_obj.get("snippet", "")).lower()
    body = _safe_text(email_obj.get("body", "")).lower()
    sender = _safe_text(email_obj.get("sender", "")).lower()

    score = 0
    if any(keyword in subject for keyword in ACTION_KEYWORDS):
        score += 30
    if any(keyword in snippet for keyword in ACTION_KEYWORDS):
        score += 20
    if any(keyword in body for keyword in ACTION_KEYWORDS):
        score += 20
    if any(token in sender for token in ["client", "customer", "partner", "vendor"]):
        score += 10
    return score


def extract_email_actions(emails, max_items=5):
    items = []
    for email_obj in emails or []:
        score = _email_action_score(email_obj)
        if score <= 0:
            continue

        sender_name, sender_email = parseaddr(_safe_text(email_obj.get("sender", ""), max_len=240))
        title = _safe_text(email_obj.get("subject", "(no subject)"), max_len=180)
        if sender_name and sender_email:
            owner = sender_name
        else:
            owner = sender_email or sender_name or "Email sender"

        items.append({
            "source": "email",
            "title": title,
            "owner": owner,
            "due_date": "",
            "priority": "medium",
            "score": score,
            "reason": f"email from {_safe_text(email_obj.get('sender', 'Unknown'), max_len=80)}",
        })

    items.sort(key=lambda item: item.get("score", 0), reverse=True)
    return items[:max_items]


def extract_slack_actions(slack_context, max_items=5):
    if not slack_context:
        return []

    items = []
    current_channel = "Slack"
    capture_action_lines = False

    for raw_line in str(slack_context).splitlines():
        line = raw_line.strip()
        if not line:
            capture_action_lines = False
            continue

        channel_match = re.match(r"^📌\s*#(.+?):$", line)
        if channel_match:
            current_channel = f"Slack #{channel_match.group(1)}"
            capture_action_lines = False
            continue

        if line.startswith("Action items:"):
            capture_action_lines = True
            continue

        if line.startswith("Decisions made:") or line.startswith("Unresolved threads:"):
            capture_action_lines = False
            continue

        if capture_action_lines and line.startswith("•"):
            item_text = line.lstrip("•").strip()
            if item_text:
                items.append({
                    "source": "slack",
                    "title": item_text,
                    "owner": current_channel,
                    "due_date": "",
                    "priority": "medium",
                    "score": 35,
                    "reason": "Slack action item",
                })

    return _dedupe_items(items)[:max_items]


def extract_pending_reply_actions(queue, max_items=5):
    items = []
    for draft in queue.get("drafts", []):
        if draft.get("status") != "needs_approval":
            continue
        items.append({
            "source": "reply_draft",
            "title": _safe_text(draft.get("reply_subject", "Reply draft"), max_len=180),
            "owner": _safe_text(draft.get("original_sender", draft.get("to", "")), max_len=120),
            "due_date": "",
            "priority": "high",
            "score": 45,
            "reason": "awaiting approval before send",
        })
    return items[:max_items]


def build_action_register(tasks_df, emails=None, slack_context="", quick_response_queue=None, max_items=12):
    queue = quick_response_queue or {"drafts": []}
    items = []
    items.extend(extract_pending_reply_actions(queue, max_items=max_items))
    items.extend(extract_task_actions(tasks_df, max_items=max_items))
    items.extend(extract_email_actions(emails or [], max_items=max_items))
    items.extend(extract_slack_actions(slack_context, max_items=max_items))

    items.sort(key=lambda item: item.get("score", 0), reverse=True)
    items = _dedupe_items(items)[:max_items]

    counts = {
        "total": len(items),
        "tasks": sum(1 for item in items if item.get("source") == "task"),
        "emails": sum(1 for item in items if item.get("source") == "email"),
        "slack": sum(1 for item in items if item.get("source") == "slack"),
        "reply_drafts": sum(1 for item in items if item.get("source") == "reply_draft"),
    }
    summary = (
        f"Unified action register: {counts['total']} item(s) total; "
        f"{counts['reply_drafts']} reply draft(s), {counts['tasks']} task(s), "
        f"{counts['emails']} email(s), {counts['slack']} Slack item(s)."
    )

    return {
        "generated_at": _now_iso(),
        "counts": counts,
        "summary": summary,
        "items": items,
    }


def write_action_register(path="action_register.json", **kwargs):
    data = build_action_register(**kwargs)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_action_register(path="action_register.json"):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "counts": {}, "summary": "No action register yet.", "items": []}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "counts": {}, "summary": "No action register yet.", "items": []}
