import json
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_PLAN_FILE = "meeting_execution_plan.json"
DEFAULT_NOTES_FILE = "meeting_notes.txt"


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=240):
    text = str(value or "").strip()
    return text[:max_len]


def _load_text(path):
    file_path = Path(path)
    if not file_path.exists():
        return ""
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _parse_meeting_notes(notes_text):
    if not notes_text:
        return []

    lines = [line.strip() for line in notes_text.splitlines() if line.strip()]
    items = []
    current_topic = "Meeting note"
    for line in lines:
        topic_match = re.match(r"^(?:##+|Meeting:|Topic:|Agenda:)(.+)$", line, re.IGNORECASE)
        if topic_match:
            current_topic = _safe_text(topic_match.group(1), max_len=180)
            continue

        if line.startswith(('-', '*', '•')):
            text = line.lstrip('-*• ').strip()
            if not text:
                continue
            owner_match = re.search(r"\b(?:owner|assigned to|assignee)[:\-]\s*([^,;]+)", text, re.IGNORECASE)
            due_match = re.search(r"\b(?:due|deadline)[:\-]\s*([^,;]+)", text, re.IGNORECASE)
            owner = _safe_text(owner_match.group(1), max_len=100) if owner_match else "Unassigned"
            due_date = _safe_text(due_match.group(1), max_len=40) if due_match else ""
            items.append({
                "source": "meeting_notes",
                "title": _safe_text(text, max_len=180),
                "owner": owner,
                "due_date": due_date,
                "priority": "medium",
                "score": 60,
                "reason": f"captured from {current_topic}",
                "next_step": f"Confirm owner {owner} and due date {due_date or 'not stated'}.",
            })
    return items


def _items_from_action_register(action_register, max_items=5):
    items = []
    for item in (action_register or {}).get("items", []):
        title = _safe_text(item.get("title", "Action item"), max_len=180)
        owner = _safe_text(item.get("owner", "Unassigned"), max_len=100)
        score = int(item.get("score", 0))
        if score < 30:
            continue
        items.append({
            "source": f"{item.get('source', 'action')}_meeting",
            "title": title,
            "owner": owner,
            "due_date": _safe_text(item.get("due_date", ""), max_len=40),
            "priority": _safe_text(item.get("priority", "medium"), max_len=20),
            "score": 30 + min(score, 30),
            "reason": item.get("reason", "meeting-worthy action"),
            "next_step": "Confirm the owner and deadline in the next meeting or thread.",
        })
    return items[:max_items]


def _items_from_follow_up_plan(follow_up_plan, max_items=5):
    items = []
    for item in (follow_up_plan or {}).get("items", []):
        title = _safe_text(item.get("title", "Follow-up item"), max_len=180)
        owner = _safe_text(item.get("owner", "Unassigned"), max_len=100)
        items.append({
            "source": f"{item.get('source', 'follow_up')}_meeting",
            "title": title,
            "owner": owner,
            "due_date": _safe_text(item.get("due_date", ""), max_len=40),
            "priority": _safe_text(item.get("priority", "medium"), max_len=20),
            "score": min(int(item.get("score", 0)) + 10, 95),
            "reason": item.get("reason", "follow-up candidate"),
            "next_step": "Turn this into a concrete action with an owner and deadline.",
        })
    return items[:max_items]


def build_meeting_execution_plan(meeting_notes=None, action_register=None, follow_up_plan=None, max_items=10):
    notes_text = meeting_notes if meeting_notes is not None else _load_text(DEFAULT_NOTES_FILE)
    items = []
    items.extend(_parse_meeting_notes(notes_text))
    items.extend(_items_from_action_register(action_register, max_items=max_items))
    items.extend(_items_from_follow_up_plan(follow_up_plan, max_items=max_items))

    seen = set()
    deduped = []
    for item in sorted(items, key=lambda x: x.get("score", 0), reverse=True):
        key = (item.get("title", "").strip().lower(), item.get("owner", "").strip().lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    counts = {
        "total": len(deduped),
        "meeting_notes": sum(1 for item in deduped if item.get("source") == "meeting_notes"),
        "action_register": sum(1 for item in deduped if item.get("source", "").endswith("_meeting") and item.get("source", "").startswith(("task", "email", "slack"))),
        "follow_up": sum(1 for item in deduped if item.get("source", "").endswith("_meeting") and item.get("source", "").startswith(("task_followup", "reply_draft", "email_followup", "slack_followup"))),
    }
    summary = (
        f"Meeting-to-execution: {counts['total']} item(s) ready; "
        f"{counts['meeting_notes']} from notes, {counts['action_register']} from the action register, "
        f"{counts['follow_up']} from follow-up autopilot."
    )
    return {
        "generated_at": _now_iso(),
        "counts": counts,
        "summary": summary,
        "items": deduped[:max_items],
    }


def write_meeting_execution_plan(path=DEFAULT_PLAN_FILE, **kwargs):
    data = build_meeting_execution_plan(**kwargs)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_meeting_execution_plan(path=DEFAULT_PLAN_FILE):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "counts": {}, "summary": "No meeting execution plan yet.", "items": []}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "counts": {}, "summary": "No meeting execution plan yet.", "items": []}
