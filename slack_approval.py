"""
Slack Approval Workflow — sends pending email draft approval requests
to a Slack channel with structured context. Users can approve/reject
directly from Slack by replying to the thread.
No paid Slack features required — uses free bot write permissions.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    WebClient = None

from quick_response import load_draft_queue

DEFAULT_LOG_FILE = "slack_approval_log.jsonl"


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=240):
    return str(value or "").strip()[:max_len]


def _get_client():
    if not WebClient:
        return None
    token = os.getenv("SLACK_BOT_TOKEN", "").strip()
    if not token:
        return None
    return WebClient(token=token)


def _build_approval_message(draft):
    subject = _safe_text(draft.get("subject", "(no subject)"), max_len=100)
    recipient = _safe_text(draft.get("recipient", "unknown"), max_len=120)
    body = _safe_text(draft.get("body", ""), max_len=300)
    draft_id = _safe_text(draft.get("id", ""), max_len=80)
    reason = _safe_text(draft.get("reason", "email reply"), max_len=120)

    return (
        f"*📋 Draft approval needed*\n"
        f"*To:* {recipient}\n"
        f"*Subject:* {subject}\n"
        f"*Reason:* {reason}\n"
        f"*Preview:* _{body[:200]}{'…' if len(body) > 200 else ''}_\n"
        f"*Draft ID:* `{draft_id}`\n"
        f"Reply `approve {draft_id}` or `reject {draft_id}` in this thread."
    )


def send_pending_approvals_to_slack(channel=None, queue_path="response_drafts.json", log_path=DEFAULT_LOG_FILE):
    """
    Post pending draft approvals to a Slack channel.
    Returns a summary dict with counts.
    """
    channel = channel or os.getenv("SLACK_APPROVAL_CHANNEL", "").strip()
    if not channel:
        return {"sent": 0, "skipped": 0, "error": "SLACK_APPROVAL_CHANNEL not set"}

    client = _get_client()
    if not client:
        return {"sent": 0, "skipped": 0, "error": "Slack client unavailable (check SLACK_BOT_TOKEN)"}

    queue = load_draft_queue(queue_path)
    pending = [d for d in queue.get("drafts", []) if d.get("status") == "needs_approval"]

    if not pending:
        return {"sent": 0, "skipped": 0, "error": None, "note": "No pending drafts to send"}

    sent = 0
    skipped = 0
    log_entries = []

    for draft in pending:
        message_text = _build_approval_message(draft)
        try:
            result = client.chat_postMessage(channel=channel, text=message_text, mrkdwn=True)
            sent += 1
            log_entries.append({
                "sent_at": _now_iso(),
                "draft_id": draft.get("id", ""),
                "channel": channel,
                "ts": result.get("ts", ""),
                "status": "sent",
            })
        except SlackApiError as e:
            skipped += 1
            log_entries.append({
                "sent_at": _now_iso(),
                "draft_id": draft.get("id", ""),
                "channel": channel,
                "status": "error",
                "error": str(e)[:200],
            })

    # Append to log
    with open(log_path, "a", encoding="utf-8") as f:
        for entry in log_entries:
            f.write(json.dumps(entry) + "\n")

    return {"sent": sent, "skipped": skipped, "error": None}


def build_slack_approval_summary(queue_path="response_drafts.json", log_path=DEFAULT_LOG_FILE):
    """
    Build a summary of the Slack approval workflow state.
    """
    queue = load_draft_queue(queue_path)
    drafts = queue.get("drafts", [])
    pending = [d for d in drafts if d.get("status") == "needs_approval"]

    # Read log for sent notifications
    sent_ids = set()
    if Path(log_path).exists():
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if entry.get("status") == "sent":
                        sent_ids.add(entry.get("draft_id", ""))
                except Exception:
                    pass

    notified = [d for d in pending if d.get("id", "") in sent_ids]
    not_notified = [d for d in pending if d.get("id", "") not in sent_ids]

    channel = os.getenv("SLACK_APPROVAL_CHANNEL", "(not configured)")
    if len(pending) == 0:
        summary = "Slack approval workflow: no pending drafts."
    else:
        summary = (
            f"Slack approval workflow: {len(pending)} pending; "
            f"{len(notified)} notified in Slack ({channel}); "
            f"{len(not_notified)} awaiting notification."
        )

    return {
        "generated_at": _now_iso(),
        "summary": summary,
        "pending_count": len(pending),
        "notified_count": len(notified),
        "not_notified_count": len(not_notified),
        "channel": channel,
    }
