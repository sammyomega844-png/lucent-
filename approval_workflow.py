import json
from datetime import datetime, timezone
from pathlib import Path

from quick_response import load_draft_queue, approve_draft, reject_draft, send_approved_drafts


DEFAULT_WORKFLOW_FILE = "approval_workflow.json"


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=240):
    text = str(value or "").strip()
    return text[:max_len]


def build_approval_workflow_report(max_items=10):
    """
    Fetch pending approvals from quick_response and build a workflow snapshot.
    Returns counts, prioritized list, and summary.
    """
    queue = load_draft_queue()
    drafts = queue.get("drafts", [])

    pending = [d for d in drafts if d.get("status") == "needs_approval"]
    approved = [d for d in drafts if d.get("status") == "approved"]
    rejected = [d for d in drafts if d.get("status") == "rejected"]
    sent = [d for d in drafts if d.get("status") == "sent"]

    # Prioritize: newer first, then high-priority recipients
    pending_sorted = sorted(
        pending,
        key=lambda d: (
            d.get("created_at", ""),
        ),
        reverse=True,
    )
    pending_top = pending_sorted[:max_items]

    items = []
    for draft in pending_top:
        recipient = _safe_text(draft.get("recipient", "unknown"), max_len=160)
        subject = _safe_text(draft.get("subject", "(no subject)"), max_len=180)
        body_preview = _safe_text(draft.get("body", ""), max_len=120)
        if len(body_preview) > 100:
            body_preview = body_preview[:100] + "…"

        items.append({
            "draft_id": draft.get("id", ""),
            "recipient": recipient,
            "subject": subject,
            "body_preview": body_preview,
            "created_at": draft.get("created_at", ""),
            "reason": draft.get("reason", "email reply"),
            "status": "needs_approval",
            "next_action": "Review and approve to send",
        })

    counts = {
        "total_pending": len(pending),
        "total_approved": len(approved),
        "total_rejected": len(rejected),
        "total_sent": len(sent),
        "showing": len(items),
    }

    if counts["total_pending"] == 0:
        summary = "Approval workflow: no pending drafts."
    else:
        summary_bits = [
            f"Approval workflow: {counts['total_pending']} draft(s) pending",
            f"{counts['total_approved']} approved",
            f"{counts['total_rejected']} rejected",
            f"{counts['total_sent']} sent",
        ]
        if items:
            top_draft = items[0]
            summary_bits.append(f"next: {top_draft['subject'][:40]} to {top_draft['recipient'].split('@')[0] if '@' in top_draft['recipient'] else top_draft['recipient']}")
        summary = "; ".join(summary_bits) + "."

    return {
        "generated_at": _now_iso(),
        "summary": summary,
        "counts": counts,
        "items": items,
    }


def approve_draft_in_workflow(draft_id, queue_path="response_drafts.json"):
    """
    Approve a single draft by ID. Updates the queue file.
    """
    queue = load_draft_queue(queue_path)
    drafts = queue.get("drafts", [])

    updated = False
    for draft in drafts:
        if draft.get("id") == draft_id:
            draft["status"] = "approved"
            draft["approved_at"] = _now_iso()
            updated = True
            break

    if updated:
        Path(queue_path).write_text(json.dumps(queue, indent=2), encoding="utf-8")
    return updated


def reject_draft_in_workflow(draft_id, reason="user rejected", queue_path="response_drafts.json"):
    """
    Reject a single draft by ID with optional reason. Updates the queue file.
    """
    queue = load_draft_queue(queue_path)
    drafts = queue.get("drafts", [])

    updated = False
    for draft in drafts:
        if draft.get("id") == draft_id:
            draft["status"] = "rejected"
            draft["rejected_at"] = _now_iso()
            draft["rejection_reason"] = reason
            updated = True
            break

    if updated:
        Path(queue_path).write_text(json.dumps(queue, indent=2), encoding="utf-8")
    return updated


def batch_approve_workflow(draft_ids, queue_path="response_drafts.json"):
    """
    Approve multiple drafts by ID list. Returns count of updated.
    """
    count = 0
    for draft_id in draft_ids:
        if approve_draft_in_workflow(draft_id, queue_path):
            count += 1
    return count


def send_workflow_approved_drafts(queue_path="response_drafts.json", audit_path="response_audit_log.jsonl"):
    """
    Send all approved drafts from the queue. Wrapper around quick_response.send_approved_drafts.
    """
    return send_approved_drafts(queue_path=queue_path, audit_path=audit_path)


def write_approval_workflow_report(path=DEFAULT_WORKFLOW_FILE):
    """
    Generate and write the approval workflow report to disk.
    """
    data = build_approval_workflow_report()
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_approval_workflow_report(path=DEFAULT_WORKFLOW_FILE):
    """
    Load the approval workflow report from disk.
    """
    file_path = Path(path)
    if not file_path.exists():
        return {
            "generated_at": _now_iso(),
            "summary": "No approval workflow report yet.",
            "counts": {},
            "items": [],
        }
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {
            "generated_at": _now_iso(),
            "summary": "No approval workflow report yet.",
            "counts": {},
            "items": [],
        }
