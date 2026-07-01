import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


DEFAULT_PLAN_FILE = "follow_up_plan.json"


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=240):
    text = str(value or "").strip()
    return text[:max_len]


def _parse_due_date(value):
    text = _safe_text(value, max_len=40)
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except Exception:
            continue
    return None


def _task_followup_items(tasks_df, max_items=5):
    items = []
    if tasks_df is None or getattr(tasks_df, "empty", True):
        return items

    today = datetime.now(timezone.utc).date()
    for _, row in tasks_df.iterrows():
        status = str(row.get("Status", "")).strip().lower()
        if status in {"completed", "done"}:
            continue

        due_date = _parse_due_date(row.get("Due_Date"))
        if due_date is None:
            continue

        days_overdue = (today - due_date).days
        if days_overdue < 0:
            continue

        title = _safe_text(row.get("Task_Name", "Untitled task"), max_len=180)
        owner = _safe_text(row.get("Assignee", "Unassigned"), max_len=100)
        items.append({
            "source": "task",
            "title": title,
            "owner": owner,
            "due_date": due_date.isoformat(),
            "priority": _safe_text(row.get("Priority", ""), max_len=20),
            "score": 60 + min(days_overdue * 5, 20),
            "reason": f"overdue by {days_overdue} day(s)",
            "nudge_subject": f"Follow up: {title}",
            "nudge_body": (
                f"Hi {owner}, just following up on {title}. "
                f"It was due on {due_date.isoformat()} and is now {days_overdue} day(s) overdue. "
                "Please send a quick status update or confirm the new deadline."
            ),
        })

    items.sort(key=lambda item: item.get("score", 0), reverse=True)
    return items[:max_items]


def _reply_followup_items(quick_response_queue, max_items=5):
    items = []
    for draft in (quick_response_queue or {}).get("drafts", []):
        if draft.get("status") != "needs_approval":
            continue
        owner = _safe_text(draft.get("original_sender", draft.get("to", "")), max_len=100)
        title = _safe_text(draft.get("reply_subject", "Reply draft"), max_len=180)
        items.append({
            "source": "reply_draft",
            "title": title,
            "owner": owner,
            "due_date": "",
            "priority": "high",
            "score": 80,
            "reason": "reply draft waiting for approval",
            "nudge_subject": f"Approval needed: {title}",
            "nudge_body": (
                f"A reply draft is waiting for approval for {owner}. "
                f"Subject: {title}. Please review and approve or revise so it can be sent."
            ),
        })
    return items[:max_items]


def _action_register_followups(action_register, max_items=6):
    items = []
    for item in (action_register or {}).get("items", []):
        source = item.get("source")
        title = _safe_text(item.get("title", "Action item"), max_len=180)
        owner = _safe_text(item.get("owner", ""), max_len=100)
        score = int(item.get("score", 0))
        if source == "task" and score >= 30:
            items.append({
                "source": "task_followup",
                "title": title,
                "owner": owner,
                "due_date": _safe_text(item.get("due_date", ""), max_len=40),
                "priority": _safe_text(item.get("priority", ""), max_len=20),
                "score": 40 + min(score, 30),
                "reason": item.get("reason", "needs follow-up"),
                "nudge_subject": f"Follow up: {title}",
                "nudge_body": (
                    f"Hi {owner}, checking in on {title}. "
                    f"It is still active in the action register because it needs attention. "
                    "Please share a status update or next step."
                ),
            })
        elif source in {"email", "slack"} and score >= 35:
            items.append({
                "source": f"{source}_followup",
                "title": title,
                "owner": owner,
                "due_date": _safe_text(item.get("due_date", ""), max_len=40),
                "priority": _safe_text(item.get("priority", "medium"), max_len=20),
                "score": 35 + min(score, 20),
                "reason": item.get("reason", "needs response"),
                "nudge_subject": f"Follow up: {title}",
                "nudge_body": (
                    f"Hi {owner}, following up on {title}. "
                    "This remains open across the current workstream. "
                    "Please confirm the next step or owner."
                ),
            })
    items.sort(key=lambda item: item.get("score", 0), reverse=True)
    return items[:max_items]


def build_follow_up_plan(tasks_df, action_register=None, quick_response_queue=None, max_items=10):
    items = []
    items.extend(_reply_followup_items(quick_response_queue, max_items=max_items))
    items.extend(_task_followup_items(tasks_df, max_items=max_items))
    items.extend(_action_register_followups(action_register, max_items=max_items))

    seen = set()
    deduped = []
    for item in sorted(items, key=lambda x: x.get("score", 0), reverse=True):
        key = (item.get("source", ""), item.get("title", "").strip().lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    counts = {
        "total": len(deduped),
        "tasks": sum(1 for item in deduped if item.get("source") in {"task", "task_followup"}),
        "reply_drafts": sum(1 for item in deduped if item.get("source") == "reply_draft"),
        "email_slack": sum(1 for item in deduped if item.get("source") in {"email_followup", "slack_followup"}),
    }
    summary = (
        f"Follow-up autopilot: {counts['total']} item(s) ready; "
        f"{counts['reply_drafts']} approval draft(s), {counts['tasks']} overdue task(s), "
        f"{counts['email_slack']} inbox/chat follow-up(s)."
    )
    return {
        "generated_at": _now_iso(),
        "counts": counts,
        "summary": summary,
        "items": deduped[:max_items],
    }


def write_follow_up_plan(path=DEFAULT_PLAN_FILE, **kwargs):
    data = build_follow_up_plan(**kwargs)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_follow_up_plan(path=DEFAULT_PLAN_FILE):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "counts": {}, "summary": "No follow-up plan yet.", "items": []}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "counts": {}, "summary": "No follow-up plan yet.", "items": []}
