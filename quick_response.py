import json
import re
import smtplib
import uuid
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.utils import parseaddr
from pathlib import Path


DEFAULT_QUEUE_FILE = "response_drafts.json"
DEFAULT_AUDIT_FILE = "response_audit_log.jsonl"

ACTIONABLE_KEYWORDS = [
    "urgent",
    "asap",
    "follow up",
    "follow-up",
    "deadline",
    "approval",
    "review",
    "quote",
    "proposal",
    "invoice",
    "issue",
    "support",
    "request",
]


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=3000):
    text = str(value or "").strip()
    if len(text) > max_len:
        return text[:max_len]
    return text


def _extract_email_address(sender):
    _, email = parseaddr(str(sender or ""))
    if email and "@" in email:
        return email
    return ""


def _append_audit(event_type, payload, audit_path=DEFAULT_AUDIT_FILE):
    line = {
        "timestamp": _now_iso(),
        "event": event_type,
        "payload": payload,
    }
    with Path(audit_path).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(line) + "\n")


def _is_actionable_email(email_obj):
    subject = _safe_text(email_obj.get("subject", "")).lower()
    snippet = _safe_text(email_obj.get("snippet", "")).lower()
    body = _safe_text(email_obj.get("body", "")).lower()
    sender = _safe_text(email_obj.get("sender", "")).lower()

    if any(k in subject for k in ACTIONABLE_KEYWORDS):
        return True
    if any(k in snippet for k in ACTIONABLE_KEYWORDS):
        return True
    if any(k in body for k in ACTIONABLE_KEYWORDS):
        return True

    # Escalate likely customer/partner requests based on sender domain hints.
    sender_domain = sender.split("@")[-1] if "@" in sender else ""
    for domain_hint in ["client", "customer", "partner", "vendor"]:
        if domain_hint in sender_domain:
            return True

    return False


def _draft_prompt(email_obj):
    sender = _safe_text(email_obj.get("sender", "Unknown"), max_len=200)
    subject = _safe_text(email_obj.get("subject", "(no subject)"), max_len=250)
    snippet = _safe_text(email_obj.get("snippet", ""), max_len=500)
    body = _safe_text(email_obj.get("body", ""), max_len=1200)

    return f"""
You are an executive assistant drafting a professional business email response.

Reply requirements:
- Tone: warm, concise, confident.
- Keep under 140 words.
- Include clear next step and timeline if possible.
- Do not invent facts not present in the original message.
- Return only the email body text (no subject line).

Incoming email:
From: {sender}
Subject: {subject}
Snippet: {snippet}
Body: {body}
""".strip()


def _fallback_draft(email_obj):
    subject = _safe_text(email_obj.get("subject", "your message"), max_len=120)
    return (
        f"Thanks for your message regarding '{subject}'. "
        "I have reviewed it and will come back with a full update shortly. "
        "If there is a hard deadline, please share it and I will prioritize accordingly."
    )


def load_draft_queue(queue_path=DEFAULT_QUEUE_FILE):
    path = Path(queue_path)
    if not path.exists():
        return {"generated_at": _now_iso(), "drafts": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "drafts": []}


def save_draft_queue(queue, queue_path=DEFAULT_QUEUE_FILE):
    Path(queue_path).write_text(json.dumps(queue, indent=2), encoding="utf-8")
    return queue_path


def create_approval_drafts(
    emails,
    ai_generate,
    max_drafts=5,
    queue_path=DEFAULT_QUEUE_FILE,
    audit_path=DEFAULT_AUDIT_FILE,
):
    drafts = []
    for email_obj in emails:
        if len(drafts) >= max_drafts:
            break
        if not _is_actionable_email(email_obj):
            continue

        to_email = _extract_email_address(email_obj.get("sender", ""))
        if not to_email:
            continue

        prompt = _draft_prompt(email_obj)
        try:
            body = _safe_text(ai_generate(prompt), max_len=2000)
        except Exception:
            body = ""

        if not body:
            body = _fallback_draft(email_obj)

        draft = {
            "id": str(uuid.uuid4()),
            "created_at": _now_iso(),
            "status": "needs_approval",
            "mode": "approval_required",
            "to": to_email,
            "original_sender": _safe_text(email_obj.get("sender", ""), max_len=240),
            "original_subject": _safe_text(email_obj.get("subject", ""), max_len=240),
            "reply_subject": f"Re: {_safe_text(email_obj.get('subject', '(no subject)'), max_len=220)}",
            "draft_body": body,
        }
        drafts.append(draft)
        _append_audit("draft_created", {"draft_id": draft["id"], "to": draft["to"]}, audit_path)

    queue = {
        "generated_at": _now_iso(),
        "drafts": drafts,
    }
    save_draft_queue(queue, queue_path)
    return queue


def approve_draft(draft_id, approved_by="owner", queue_path=DEFAULT_QUEUE_FILE, audit_path=DEFAULT_AUDIT_FILE):
    queue = load_draft_queue(queue_path)
    for draft in queue.get("drafts", []):
        if draft.get("id") == draft_id:
            draft["status"] = "approved"
            draft["approved_by"] = approved_by
            draft["approved_at"] = _now_iso()
            save_draft_queue(queue, queue_path)
            _append_audit("draft_approved", {"draft_id": draft_id, "approved_by": approved_by}, audit_path)
            return True
    return False


def reject_draft(draft_id, reason="rejected", queue_path=DEFAULT_QUEUE_FILE, audit_path=DEFAULT_AUDIT_FILE):
    queue = load_draft_queue(queue_path)
    for draft in queue.get("drafts", []):
        if draft.get("id") == draft_id:
            draft["status"] = "rejected"
            draft["rejected_reason"] = _safe_text(reason, max_len=220)
            draft["rejected_at"] = _now_iso()
            save_draft_queue(queue, queue_path)
            _append_audit("draft_rejected", {"draft_id": draft_id, "reason": reason}, audit_path)
            return True
    return False


def send_approved_drafts(
    smtp_host,
    smtp_port,
    smtp_username,
    smtp_password,
    from_email,
    queue_path=DEFAULT_QUEUE_FILE,
    audit_path=DEFAULT_AUDIT_FILE,
):
    queue = load_draft_queue(queue_path)
    approved = [d for d in queue.get("drafts", []) if d.get("status") == "approved"]
    if not approved:
        return {"sent": 0, "failed": 0}

    sent = 0
    failed = 0

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    try:
        for draft in approved:
            try:
                msg = MIMEText(draft.get("draft_body", ""), "plain", "utf-8")
                msg["From"] = from_email
                msg["To"] = draft.get("to", "")
                msg["Subject"] = draft.get("reply_subject", "Re: Update")
                server.sendmail(from_email, [draft.get("to", "")], msg.as_string())
                draft["status"] = "sent"
                draft["sent_at"] = _now_iso()
                sent += 1
                _append_audit("draft_sent", {"draft_id": draft.get("id"), "to": draft.get("to")}, audit_path)
            except Exception as exc:
                failed += 1
                draft["status"] = "send_failed"
                draft["send_error"] = _safe_text(exc, max_len=250)
                _append_audit(
                    "draft_send_failed",
                    {"draft_id": draft.get("id"), "error": _safe_text(exc, max_len=250)},
                    audit_path,
                )
    finally:
        server.quit()

    save_draft_queue(queue, queue_path)
    return {"sent": sent, "failed": failed}


def summarize_queue(queue):
    drafts = queue.get("drafts", [])
    total = len(drafts)
    approved = sum(1 for d in drafts if d.get("status") == "approved")
    pending = sum(1 for d in drafts if d.get("status") == "needs_approval")
    sent = sum(1 for d in drafts if d.get("status") == "sent")
    return (
        f"QUICK RESPONSE DRAFTS: total={total}, pending_approval={pending}, "
        f"approved={approved}, sent={sent}."
    )


def list_pending_drafts(queue_path=DEFAULT_QUEUE_FILE):
    queue = load_draft_queue(queue_path)
    return [d for d in queue.get("drafts", []) if d.get("status") == "needs_approval"]
