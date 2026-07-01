"""
Recommendations Engine — generates smart, pattern-based recommendations
from tasks, CRM, follow-up, pipeline risk, and customer health signals.
No AI call required: uses rule-based heuristics over existing artifacts.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REPORT_FILE = "recommendations.json"


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value, max_len=240):
    return str(value or "").strip()[:max_len]


def _rec(category, title, rationale, action, priority="medium"):
    return {
        "category": category,
        "title": title,
        "rationale": rationale,
        "action": action,
        "priority": priority,
    }


def build_recommendations(
    action_register=None,
    follow_up_plan=None,
    customer_health_report=None,
    pipeline_risk_report=None,
    kpi_digest=None,
    approval_workflow_report=None,
):
    recs = []

    # ── Action register signals ──────────────────────────────
    ar_items = (action_register or {}).get("items", [])
    high_score_items = [i for i in ar_items if i.get("score", 0) >= 70]
    if high_score_items:
        top = high_score_items[0]
        recs.append(_rec(
            "action",
            f"Prioritise: {_safe_text(top.get('title', 'top action'), max_len=60)}",
            f"This item has a score of {top.get('score', '?')}/100 in the action register.",
            f"Assign to {_safe_text(top.get('owner', 'the right owner'))} and set a deadline today.",
            priority="high",
        ))

    overdue_count = sum(1 for i in ar_items if "overdue" in _safe_text(i.get("reason", "")).lower())
    if overdue_count >= 2:
        recs.append(_rec(
            "action",
            f"Clear {overdue_count} overdue items today",
            "Multiple overdue action items are building up and creating a backlog.",
            "Block 30 minutes to close or re-assign each overdue item.",
            priority="high",
        ))

    # ── Follow-up signals ────────────────────────────────────
    fu_items = (follow_up_plan or {}).get("items", [])
    stale_approvals = [i for i in fu_items if "approval" in _safe_text(i.get("reason", "")).lower()]
    if stale_approvals:
        recs.append(_rec(
            "email",
            f"Approve {len(stale_approvals)} waiting email draft(s)",
            "Reply drafts are sitting in the approval queue and blocking outbound communication.",
            "Open the approval workflow section and review each draft.",
            priority="high",
        ))

    # ── Customer health signals ──────────────────────────────
    ch_items = (customer_health_report or {}).get("items", [])
    risk_accounts = [i for i in ch_items if i.get("bucket") == "risk"]
    healthy_accounts = [i for i in ch_items if i.get("bucket") == "healthy"]

    if risk_accounts:
        top_risk = risk_accounts[0]
        recs.append(_rec(
            "crm",
            f"Re-engage {_safe_text(top_risk.get('company', ''), max_len=40)} before it goes cold",
            f"This account scored {top_risk.get('score', '?')}/100 — risk bucket, "
            f"{_safe_text(top_risk.get('reason', ''), max_len=80)}.",
            "Send a personal touchpoint email and update the CRM last contact date.",
            priority="high",
        ))

    if len(risk_accounts) >= 3:
        recs.append(_rec(
            "crm",
            f"Review {len(risk_accounts)} at-risk accounts this week",
            "A cluster of accounts is deteriorating simultaneously, which may indicate a systemic gap.",
            "Schedule a 30-minute review of the customer health radar and update outreach plans.",
            priority="medium",
        ))

    if healthy_accounts:
        top_opp = healthy_accounts[0]
        recs.append(_rec(
            "crm",
            f"Expand {_safe_text(top_opp.get('company', ''), max_len=40)} while momentum is high",
            f"This account scored {top_opp.get('score', '?')}/100 — strong engagement, qualified status.",
            "Propose an upsell or referral conversation while the relationship is warm.",
            priority="medium",
        ))

    # ── Pipeline risk signals ────────────────────────────────
    pr_items = (pipeline_risk_report or {}).get("items", [])
    slipping_deals = [i for i in pr_items if i.get("bucket") == "risk"]

    if slipping_deals:
        top_slip = slipping_deals[0]
        value = top_slip.get("lead_value", 0)
        recs.append(_rec(
            "pipeline",
            f"Escalate {_safe_text(top_slip.get('company', ''), max_len=40)} — deal is slipping",
            f"This deal (${value:,.0f}) has a pipeline risk score of {top_slip.get('score', '?')}/100 "
            f"({_safe_text(top_slip.get('reason', ''), max_len=80)}).",
            "Reset the close plan, confirm stakeholder availability, and set a hard next-step date.",
            priority="high",
        ))

    stale_deals = [i for i in pr_items if i.get("bucket") in ("risk", "watch")]
    if len(stale_deals) >= 2:
        total_value = sum(i.get("lead_value", 0) for i in stale_deals)
        recs.append(_rec(
            "pipeline",
            f"${total_value:,.0f} in pipeline needs attention this week",
            f"{len(stale_deals)} deals are in risk or watch — combined value at risk.",
            "Block time for a pipeline review; advance or close each deal this week.",
            priority="medium",
        ))

    # ── KPI digest signals ───────────────────────────────────
    kpi_flags = (kpi_digest or {}).get("flags", [])
    for flag in kpi_flags[:2]:
        recs.append(_rec(
            "kpi",
            f"KPI regression: {flag[:60]}",
            "A key metric is trending in the wrong direction over the past two weeks.",
            "Investigate the root cause and add a corrective action to this week's priorities.",
            priority="medium",
        ))

    # ── Approval workflow signals ─────────────────────────────
    aw_counts = (approval_workflow_report or {}).get("counts", {})
    pending_count = aw_counts.get("total_pending", 0)
    if pending_count >= 3:
        recs.append(_rec(
            "email",
            f"Batch-approve {pending_count} pending email drafts",
            "A queue of drafts is growing. Delay in approval stalls outbound communication.",
            "Spend 10 minutes reviewing and approving or rejecting each draft in bulk.",
            priority="medium",
        ))

    # Sort: high first, then medium
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recs.sort(key=lambda r: priority_order.get(r["priority"], 2))

    high_count = sum(1 for r in recs if r["priority"] == "high")
    medium_count = sum(1 for r in recs if r["priority"] == "medium")

    if not recs:
        summary = "Recommendations: no urgent patterns detected — all signals look stable."
    else:
        summary = (
            f"Recommendations: {len(recs)} action(s) suggested; "
            f"{high_count} high-priority, {medium_count} medium-priority."
        )
        if recs:
            summary += f" Top: {recs[0]['title'][:60]}."

    return {
        "generated_at": _now_iso(),
        "summary": summary,
        "counts": {"total": len(recs), "high": high_count, "medium": medium_count},
        "items": recs,
    }


def write_recommendations(path=DEFAULT_REPORT_FILE, **kwargs):
    data = build_recommendations(**kwargs)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_recommendations(path=DEFAULT_REPORT_FILE):
    file_path = Path(path)
    if not file_path.exists():
        return {"generated_at": _now_iso(), "summary": "No recommendations yet.", "counts": {}, "items": []}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": _now_iso(), "summary": "No recommendations yet.", "counts": {}, "items": []}
