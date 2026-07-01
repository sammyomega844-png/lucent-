"""
Email Sentiment Flagging — scores emails by urgency and emotional
tone, returns a prioritised list of emails that need immediate attention
vs those that are routine. No paid NLP APIs required.
"""

import re
from datetime import datetime, timezone

DEFAULT_URGENT_THRESHOLD = 60  # score out of 100

# Keyword banks — weighted by severity
URGENT_SIGNALS = [
    (20, ["urgent", "asap", "immediately", "critical", "emergency"]),
    (15, ["action required", "response required", "must respond", "needs your approval"]),
    (12, ["overdue", "past due", "deadline", "expiring", "expires today"]),
    (10, ["important", "time-sensitive", "priority", "cannot wait", "follow up"]),
    (8,  ["please advise", "waiting on you", "blocked", "escalate", "escalation"]),
    (6,  ["concerned", "unhappy", "frustrated", "disappointed", "issue", "problem"]),
    (4,  ["confirm", "clarify", "update", "status", "reply needed"]),
]

ROUTINE_SIGNALS = [
    (-10, ["newsletter", "unsubscribe", "no-reply", "noreply", "digest", "weekly update"]),
    (-8,  ["fyi", "heads up", "just sharing", "thought you'd like", "no action needed"]),
    (-6,  ["invitation", "reminder", "calendar", "scheduling"]),
]


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=2000):
    return str(value or "").strip()[:max_len]


def _score_email(email):
    subject = _safe_text(email.get("subject", ""), max_len=200).lower()
    body = _safe_text(email.get("body", ""), max_len=1000).lower()
    sender = _safe_text(email.get("from", ""), max_len=200).lower()
    text = subject + " " + body + " " + sender

    score = 30  # baseline
    matched_signals = []

    for weight, keywords in URGENT_SIGNALS:
        for kw in keywords:
            if kw in text:
                score += weight
                matched_signals.append(kw)
                break  # one match per group

    for weight, keywords in ROUTINE_SIGNALS:
        for kw in keywords:
            if kw in text:
                score += weight
                matched_signals.append(f"({kw})")
                break

    # Subject line emphasis — double weight for subject matches
    for weight, keywords in URGENT_SIGNALS:
        for kw in keywords:
            if kw in subject:
                score += weight // 2  # bonus for subject match
                break

    score = max(0, min(100, score))

    if score >= DEFAULT_URGENT_THRESHOLD:
        flag = "urgent"
    elif score >= 40:
        flag = "review"
    else:
        flag = "routine"

    return score, flag, matched_signals[:5]


def flag_emails(emails):
    """
    Score and flag a list of email dicts.
    Returns sorted list with scores and flags.
    """
    if not emails:
        return []

    flagged = []
    for email in emails:
        score, flag, signals = _score_email(email)
        flagged.append({
            "subject": _safe_text(email.get("subject", "(no subject)"), max_len=100),
            "from": _safe_text(email.get("from", "unknown"), max_len=100),
            "date": _safe_text(email.get("date", ""), max_len=40),
            "score": score,
            "flag": flag,
            "signals": signals,
            "body_preview": _safe_text(email.get("body", ""), max_len=120),
        })

    flagged.sort(key=lambda e: e["score"], reverse=True)
    return flagged


def build_sentiment_report(emails):
    """
    Build a full sentiment flagging report from an email list.
    """
    if not emails:
        return {
            "generated_at": _now_iso(),
            "summary": "Email sentiment: no emails to analyse.",
            "counts": {"total": 0, "urgent": 0, "review": 0, "routine": 0},
            "items": [],
        }

    flagged = flag_emails(emails)
    urgent = [e for e in flagged if e["flag"] == "urgent"]
    review = [e for e in flagged if e["flag"] == "review"]
    routine = [e for e in flagged if e["flag"] == "routine"]

    counts = {
        "total": len(flagged),
        "urgent": len(urgent),
        "review": len(review),
        "routine": len(routine),
    }

    if counts["urgent"] > 0:
        top_urgent = urgent[0]
        summary = (
            f"Email sentiment: {counts['total']} email(s) analysed; "
            f"{counts['urgent']} urgent, {counts['review']} for review, {counts['routine']} routine. "
            f"Top urgent: \"{top_urgent['subject'][:50]}\" from {top_urgent['from'][:30]}."
        )
    elif counts["review"] > 0:
        summary = (
            f"Email sentiment: {counts['total']} email(s) analysed; "
            f"0 urgent, {counts['review']} for review, {counts['routine']} routine."
        )
    else:
        summary = (
            f"Email sentiment: {counts['total']} email(s) analysed — "
            f"all routine, no immediate action needed."
        )

    return {
        "generated_at": _now_iso(),
        "summary": summary,
        "counts": counts,
        "items": flagged,
    }
