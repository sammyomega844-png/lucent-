import html
import json
from datetime import datetime
from pathlib import Path

from setup_wizard import build_setup_summary, write_setup_wizard
from action_register import load_action_register
from follow_up import load_follow_up_plan
from meeting_pipeline import load_meeting_execution_plan
from customer_health import load_customer_health_report
from pipeline_risk import load_pipeline_risk_report
from approval_workflow import load_approval_workflow_report
from kpi_digest import load_kpi_digest
from communication_timeline import load_communication_timeline
from recommendations import load_recommendations
from revenue_forecast import load_revenue_forecast
from deal_progression import load_deal_progression
from renewal_reminders import load_renewal_reminders


THEME = {
    "ink": "#0f172a",
    "muted": "#64748b",
    "bg": "linear-gradient(135deg, #f5efe6 0%, #edf4fb 48%, #f7f7fb 100%)",
    "card": "rgba(255,255,255,0.82)",
    "border": "rgba(15, 23, 42, 0.10)",
    "accent": "#c2410c",
    "accent2": "#0f766e",
    "accent3": "#1d4ed8",
    "good": "#15803d",
    "watch": "#b45309",
    "risk": "#b91c1c",
}


def _read_text(path, fallback=""):
    file_path = Path(path)
    if not file_path.exists():
        return fallback
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception:
        return fallback


def _read_json(path, fallback=None):
    file_path = Path(path)
    if not file_path.exists():
        return fallback if fallback is not None else {}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return fallback if fallback is not None else {}


def _extract_between(text, start_marker, end_marker, fallback=""):
    if start_marker not in text or end_marker not in text:
        return fallback
    try:
        start = text.index(start_marker) + len(start_marker)
        end = text.index(end_marker, start)
        return text[start:end].strip()
    except ValueError:
        return fallback


def _latest_snapshot():
    snapshots = sorted(Path(".").glob("snapshot_*.json"), reverse=True)
    for snapshot in snapshots:
        try:
            return json.loads(snapshot.read_text(encoding="utf-8"))
        except Exception:
            continue
    return {}


def _score_class(score):
    if score >= 80:
        return "good"
    if score >= 60:
        return "watch"
    return "risk"


def _status_badge(label):
    if label.lower().startswith("good") or label.lower().startswith("market strength"):
        return "good"
    if label.lower().startswith("needs") or label.lower().startswith("mixed"):
        return "watch"
    return "risk"


def _metric_card(label, value, hint=""):
    return f"""
    <article class=\"metric\">
      <div class=\"metric-label\">{html.escape(label)}</div>
      <div class=\"metric-value\">{html.escape(str(value))}</div>
      <div class=\"metric-hint\">{html.escape(hint)}</div>
    </article>
    """


def build_dashboard_html():
    weekly = _read_json("weekly_digest.json", {})
    status_html = _read_text("project_status.html", "")
    briefing_html = _read_text("executive_briefing.html", "")
    setup_summary = build_setup_summary()
    latest_snapshot = _latest_snapshot()
    action_register = load_action_register()
    action_items = action_register.get("items", [])
    action_summary = action_register.get("summary", "Unified action register: not generated yet.")
    follow_up_plan = load_follow_up_plan()
    follow_up_summary = follow_up_plan.get("summary", "No follow-up plan yet.")
    follow_up_items = follow_up_plan.get("items", [])
    meeting_execution_plan = load_meeting_execution_plan()
    meeting_execution_summary = meeting_execution_plan.get("summary", "No meeting execution plan yet.")
    meeting_execution_items = meeting_execution_plan.get("items", [])
    customer_health_report = load_customer_health_report()
    customer_health_summary = customer_health_report.get("summary", "No customer health report yet.")
    customer_health_items = customer_health_report.get("items", [])
    pipeline_risk_report = load_pipeline_risk_report()
    pipeline_risk_summary = pipeline_risk_report.get("summary", "No pipeline risk report yet.")
    pipeline_risk_items = pipeline_risk_report.get("items", [])
    approval_workflow_report = load_approval_workflow_report()
    approval_workflow_summary = approval_workflow_report.get("summary", "No approval workflow yet.")
    approval_workflow_items = approval_workflow_report.get("items", [])
    kpi_report = load_kpi_digest()
    kpi_summary = kpi_report.get("summary", "No KPI digest yet.")
    kpi_flags = kpi_report.get("flags", [])
    kpi_kpis = kpi_report.get("kpis", {})
    comm_timeline = load_communication_timeline()
    comm_timeline_summary = comm_timeline.get("summary", "No communication timeline yet.")
    comm_accounts = comm_timeline.get("accounts", {})
    recs_report = load_recommendations()
    recs_summary = recs_report.get("summary", "No recommendations yet.")
    recs_items = recs_report.get("items", [])
    revenue_forecast = load_revenue_forecast()
    revenue_forecast_summary = revenue_forecast.get("summary", "No revenue forecast yet.")
    revenue_horizons = revenue_forecast.get("horizons", {})
    deal_prog = load_deal_progression()
    deal_prog_summary = deal_prog.get("summary", "No deal progression data yet.")
    deal_prog_items = deal_prog.get("items", [])
    renewals = load_renewal_reminders()
    renewals_summary = renewals.get("summary", "No renewal reminders yet.")
    renewals_items = renewals.get("items", [])

    action_item_rows = []
    for item in action_items[:5]:
        action_item_rows.append(
            f"<li><strong>{html.escape(str(item.get('title', '')))}</strong>"
            f"<span class=\"footer-note\">{html.escape(str(item.get('owner', '')))} • {html.escape(str(item.get('source', '')))} • {html.escape(str(item.get('reason', '')))}</span></li>"
        )
    action_items_html = "".join(action_item_rows) if action_item_rows else "<li>No action register items yet.</li>"

    follow_up_rows = []
    for item in follow_up_items[:5]:
      follow_up_rows.append(
        f"<li><strong>{html.escape(str(item.get('nudge_subject', item.get('title', ''))))}</strong>"
        f"<span class=\"footer-note\">{html.escape(str(item.get('owner', '')))} • {html.escape(str(item.get('reason', '')))}</span></li>"
      )
    follow_up_html = "".join(follow_up_rows) if follow_up_rows else "<li>No follow-up items yet.</li>"

    meeting_rows = []
    for item in meeting_execution_items[:5]:
      meeting_rows.append(
        f"<li><strong>{html.escape(str(item.get('title', '')))}</strong>"
        f"<span class=\"footer-note\">{html.escape(str(item.get('owner', '')))} • {html.escape(str(item.get('due_date', '')))} • {html.escape(str(item.get('next_step', '')))}</span></li>"
      )
    meeting_execution_html = "".join(meeting_rows) if meeting_rows else "<li>No meeting execution items yet.</li>"

    customer_health_rows = []
    for item in customer_health_items[:5]:
      customer_health_rows.append(
        f"<li><strong>{html.escape(str(item.get('company', item.get('lead_name', ''))))}</strong>"
        f"<span class=\"footer-note\">{html.escape(str(item.get('lead_name', '')))} • {html.escape(str(item.get('bucket', '')))} • {html.escape(str(item.get('next_step', '')))}</span></li>"
      )
    customer_health_html = "".join(customer_health_rows) if customer_health_rows else "<li>No customer health items yet.</li>"

    pipeline_risk_rows = []
    for item in pipeline_risk_items[:5]:
      pipeline_risk_rows.append(
        f"<li><strong>{html.escape(str(item.get('company', item.get('lead_name', ''))))}</strong>"
        f"<span class=\"footer-note\">{html.escape(str(item.get('lead_name', '')))} • {html.escape(str(item.get('bucket', '')))} • {html.escape(str(item.get('next_step', '')))}</span></li>"
      )
    pipeline_risk_html = "".join(pipeline_risk_rows) if pipeline_risk_rows else "<li>No pipeline risk items yet.</li>"

    approval_workflow_rows = []
    for item in approval_workflow_items[:5]:
      approval_workflow_rows.append(
        f"<li><strong>{html.escape(str(item.get('subject', '')))}</strong>"
        f"<span class=\"footer-note\">{html.escape(str(item.get('recipient', '')))} • {html.escape(str(item.get('created_at', '')[-8:-3]))} • {html.escape(str(item.get('next_action', '')))}</span></li>"
      )
    approval_workflow_html = "".join(approval_workflow_rows) if approval_workflow_rows else "<li>No approval workflows yet.</li>"

    kpi_flag_rows = []
    for flag in kpi_flags[:5]:
        kpi_flag_rows.append(f"<li>{html.escape(str(flag))}</li>")
    kpi_flags_html = "".join(kpi_flag_rows) if kpi_flag_rows else "<li>All KPIs stable.</li>"

    kpi_metric_rows = []
    for key, v in list(kpi_kpis.items())[:6]:
        trend_icon = "📉" if v.get("trend") == "declining" else "📈" if v.get("trend") == "improving" else "→"
        kpi_metric_rows.append(
            f"<li><strong>{html.escape(key.replace('_', ' ').title())}</strong>"
            f"<span class=\"footer-note\">Latest: {html.escape(str(v.get('latest', '')))} • Avg: {html.escape(str(v.get('avg', '')))} • {trend_icon} {html.escape(v.get('trend', 'stable'))}</span></li>"
        )
    kpi_metrics_html = "".join(kpi_metric_rows) if kpi_metric_rows else "<li>No KPI data yet.</li>"

    recs_rows = []
    for item in recs_items[:5]:
        priority_badge = "🔴" if item.get("priority") == "high" else "🟡"
        recs_rows.append(
            f"<li><strong>{priority_badge} {html.escape(str(item.get('title', '')))}</strong>"
            f"<span class=\"footer-note\">{html.escape(str(item.get('rationale', ''))[:80])} • {html.escape(str(item.get('action', ''))[:80])}</span></li>"
        )
    recs_html = "".join(recs_rows) if recs_rows else "<li>No recommendations yet.</li>"

    timeline_rows = []
    for company, acc in list(comm_accounts.items())[:4]:
        touches = acc.get("touches", [])
        latest = touches[0].get("summary", "")[:80] if touches else "No touches recorded"
        timeline_rows.append(
            f"<li><strong>{html.escape(str(company))}</strong>"
            f"<span class=\"footer-note\">{html.escape(str(acc.get('status', '')))} • {html.escape(str(acc.get('touch_count', 0)))} touch(es) • {html.escape(latest)}</span></li>"
        )
    timeline_html = "".join(timeline_rows) if timeline_rows else "<li>No timeline data yet.</li>"

    # Revenue forecast horizon cards
    rev_horizon_rows = []
    for h in ["30", "60", "90"]:
        r = revenue_horizons.get(h, {})
        rev_horizon_rows.append(
            f"<li><strong>{html.escape(h)}-day</strong>"
            f"<span class=\"footer-note\">${r.get('projected_revenue', 0):,.0f} projected • ${r.get('best_case_revenue', 0):,.0f} best case • {r.get('deal_count', 0)} deal(s)</span></li>"
        )
    revenue_forecast_html = "".join(rev_horizon_rows) if rev_horizon_rows else "<li>No forecast data yet.</li>"

    deal_prog_rows = []
    for item in deal_prog_items[:5]:
        badge = "🔴" if item.get("stage_label") == "stuck" else "🟢"
        deal_prog_rows.append(
            f"<li><strong>{badge} {html.escape(str(item.get('company', '')))}</strong>"
            f"<span class=\"footer-note\">{html.escape(str(item.get('status', '')))} • {html.escape(str(item.get('days_since_contact', '')))}d since contact • {html.escape(str(item.get('next_step', ''))[:70])}</span></li>"
        )
    deal_prog_html = "".join(deal_prog_rows) if deal_prog_rows else "<li>No deal progression data yet.</li>"

    renewals_rows = []
    for item in renewals_items[:5]:
        urgency_icon = "🚨" if item.get("urgency") == "overdue" else "🔔" if item.get("urgency") == "this_month" else "📅"
        renewals_rows.append(
            f"<li><strong>{urgency_icon} {html.escape(str(item.get('company', '')))}</strong>"
            f"<span class=\"footer-note\">{html.escape(str(item.get('label', '')))} • {html.escape(str(item.get('renewal_date', '')))} • {html.escape(str(item.get('next_step', ''))[:70])}</span></li>"
        )
    renewals_html = "".join(renewals_rows) if renewals_rows else "<li>No renewals due in the next 90 days.</li>"

    digest_rows = []
    for row in weekly.get("rows", []):
        pipeline_value = row.get("pipeline_value", 0)
        digest_rows.append(
            f"<tr><td>{html.escape(str(row.get('date', '')))}</td>"
            f"<td>{html.escape(str(row.get('completed_tasks', '')))}</td>"
            f"<td>{html.escape(str(row.get('high_priority_open', '')))}</td>"
            f"<td>{html.escape(str(row.get('stock_alerts', '')))}</td>"
            f"<td>{html.escape(str(row.get('qualified_leads', '')))}</td>"
            f"<td>{html.escape(f'${pipeline_value:,}')}</td></tr>"
        )
    digest_rows_html = "".join(digest_rows) if digest_rows else "<tr><td colspan=6>No weekly digest data yet.</td></tr>"

    briefing_text = _extract_between(briefing_html, "<pre>", "</pre>", fallback=briefing_html)
    briefing_text = html.escape(briefing_text)

    updated_line = "Live local snapshot"
    if "STATUS_SYNC:START" in status_html and "STATUS_SYNC:END" in status_html:
        sync_text = _extract_between(status_html, "<!-- STATUS_SYNC:START -->", "<!-- STATUS_SYNC:END -->", fallback="")
        sync_text = html.unescape(sync_text)
        if sync_text:
            updated_line = sync_text.replace("<div class=\"status-sync\">", "").replace("</div>", "").strip()

    overall_score = latest_snapshot.get("overall_score", 84)
    day_rating = latest_snapshot.get("day_rating", "Good")
    market_signal_score = latest_snapshot.get("market_signal_score", 62)
    market_signal_label = latest_snapshot.get("market_signal_label", "Market strength")
    score_class = _score_class(int(overall_score))
    signal_class = _status_badge(str(market_signal_label))

    feature_count = str(status_html.count("status-card s-done")) if status_html else "0"
    digest_count = str(len(weekly.get("rows", [])))
    readiness_score = setup_summary.get("readiness_score", 0)

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Lucent — Executive Intelligence</title>
  <style>
    :root {{
      --ink: {THEME['ink']};
      --muted: {THEME['muted']};
      --bg: {THEME['bg']};
      --card: {THEME['card']};
      --border: {THEME['border']};
      --accent: {THEME['accent']};
      --accent2: {THEME['accent2']};
      --accent3: {THEME['accent3']};
      --good: {THEME['good']};
      --watch: {THEME['watch']};
      --risk: {THEME['risk']};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--bg);
      font-family: Inter, "Segoe UI", system-ui, -apple-system, sans-serif;
      min-height: 100vh;
    }}
    .shell {{ max-width: 1240px; margin: 0 auto; padding: 28px 16px 36px; }}
    .hero {{
      position: relative;
      overflow: hidden;
      border: 1px solid var(--border);
      border-radius: 28px;
      background: linear-gradient(135deg, rgba(15,23,42,.96), rgba(30,41,59,.96));
      color: #fff;
      padding: 28px;
      box-shadow: 0 24px 60px rgba(15, 23, 42, 0.18);
    }}
    .hero::after {{
      content: '';
      position: absolute;
      inset: auto -80px -120px auto;
      width: 300px;
      height: 300px;
      background: radial-gradient(circle, rgba(255,255,255,.18), transparent 68%);
      pointer-events: none;
    }}
    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(255,255,255,.09);
      border: 1px solid rgba(255,255,255,.15);
      font-size: 12px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    .hero-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.5fr) minmax(320px, 1fr);
      gap: 20px;
      margin-top: 18px;
      align-items: end;
      position: relative;
      z-index: 1;
    }}
    .hero h1 {{ margin: 10px 0 10px; font-size: clamp(30px, 4vw, 54px); line-height: 0.98; letter-spacing: -0.04em; max-width: 14ch; }}
    .hero p {{ margin: 0; color: rgba(255,255,255,.84); font-size: 15px; line-height: 1.6; max-width: 64ch; }}
    .hero-card {{
      border-radius: 22px;
      background: rgba(255,255,255,.08);
      border: 1px solid rgba(255,255,255,.12);
      padding: 18px;
      backdrop-filter: blur(10px);
    }}
    .status-line {{ color: rgba(255,255,255,.78); font-size: 12px; margin-top: 10px; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }}
    .chip {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(255,255,255,.08);
      border: 1px solid rgba(255,255,255,.12);
      font-size: 13px;
      font-weight: 600;
    }}
    .chip.good {{ border-color: color-mix(in srgb, var(--good) 80%, white); }}
    .chip.watch {{ border-color: color-mix(in srgb, var(--watch) 80%, white); }}
    .chip.risk {{ border-color: color-mix(in srgb, var(--risk) 80%, white); }}
    .section {{ margin-top: 18px; }}
    .section-head {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: end;
      margin: 22px 0 12px;
    }}
    .section-head h2 {{ margin: 0; font-size: 20px; letter-spacing: -0.02em; }}
    .section-head p {{ margin: 0; color: var(--muted); font-size: 13px; }}
    .grid {{ display: grid; gap: 14px; }}
    .metrics {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
    .workspace {{ grid-template-columns: 1.2fr .8fr; align-items: start; }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 22px;
      box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
      backdrop-filter: blur(10px);
    }}
    .metric {{ padding: 18px; }}
    .metric-label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }}
    .metric-value {{ margin-top: 8px; font-size: 30px; line-height: 1; font-weight: 800; letter-spacing: -.04em; }}
    .metric-hint {{ margin-top: 8px; color: var(--muted); font-size: 13px; line-height: 1.5; min-height: 40px; }}
    .panel {{ padding: 18px; }}
    .panel h3 {{ margin: 0; font-size: 16px; letter-spacing: -.02em; }}
    .panel p {{ color: var(--muted); line-height: 1.6; }}
    .summary-list {{ margin: 12px 0 0; padding: 0; list-style: none; display: grid; gap: 10px; }}
    .summary-list li {{
      padding: 12px 14px;
      background: rgba(15,23,42,.03);
      border: 1px solid rgba(15,23,42,.06);
      border-radius: 16px;
      line-height: 1.55;
    }}
    .summary-list strong {{ display: block; margin-bottom: 3px; color: var(--ink); }}
    .table-wrap {{ overflow: auto; border-radius: 18px; border: 1px solid var(--border); }}
    table {{ width: 100%; border-collapse: collapse; min-width: 820px; background: rgba(255,255,255,.84); }}
    th, td {{ padding: 12px 14px; text-align: left; border-bottom: 1px solid rgba(15,23,42,.06); font-size: 14px; }}
    th {{ background: rgba(15,23,42,.03); font-size: 12px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }}
    .footer-note {{ color: var(--muted); font-size: 13px; margin-top: 12px; }}
    .preview {{ white-space: pre-wrap; font-family: inherit; font-size: 14px; line-height: 1.7; margin: 0; color: var(--ink); max-height: 540px; overflow: auto; }}
    .badges {{ display: flex; flex-wrap: wrap; gap: 10px; }}
    .pill {{
      display: inline-flex;
      align-items: center;
      padding: 8px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      background: rgba(15,23,42,.05);
      border: 1px solid rgba(15,23,42,.06);
    }}
    .pill.good {{ color: var(--good); }}
    .pill.watch {{ color: var(--watch); }}
    .pill.risk {{ color: var(--risk); }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    @media (max-width: 980px) {{
      .hero-grid, .workspace, .metrics {{ grid-template-columns: 1fr; }}
      .shell {{ padding: 18px 12px 30px; }}
      .hero {{ padding: 20px; }}
    }}
  </style>
</head>
<body>
  <main class=\"shell\">
    <section class=\"hero\">
      <span class="eyebrow">Lucent</span>
      <div class=\"hero-grid\">
        <div>
          <h1>Polished, executive-ready daily intelligence.</h1>
          <p>A single client-facing view for today’s briefing, weekly trend history, delivery health, and product readiness. Built to feel credible in front of customers, not like an internal script output.</p>
          <div class=\"chips\">
            <span class=\"chip {score_class}\">Day Score {html.escape(str(overall_score))}/100</span>
            <span class=\"chip {signal_class}\">Strategic Pulse {html.escape(str(market_signal_score))}/100</span>
            <span class=\"chip\">{html.escape(str(day_rating))}</span>
            <span class=\"chip\">{html.escape(str(market_signal_label))}</span>
          </div>
        </div>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Follow-up autopilot</h2>
          <p>{html.escape(follow_up_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {follow_up_html}
        </ul>
      </div>
    </section>
        <div class=\"hero-card\">
          <div class=\"badges\">
            <span class=\"pill {score_class}\">{html.escape(str(updated_line))}</span>
            <span class=\"pill\">{html.escape(str(feature_count))} completed features</span>
            <span class=\"pill\">{html.escape(str(digest_count))} weekly digest rows</span>
          </div>
          <p class=\"status-line\">The dashboard is assembled from local files only: briefing, weekly digest, project status, and current snapshot data.</p>
        </div>
      </div>
    </section>

    <section class=\"section\">
      <div class=\"section-head\">
        <div>
          <h2>Operational pulse</h2>
          <p>At-a-glance metrics your customer will actually understand.</p>
        </div>
      </div>
      <div class=\"grid metrics\">
        { _metric_card("Latest overall score", f"{overall_score}/100", "Composite view of tasks, inventory, and CRM health.") }
        { _metric_card("Market signal", f"{market_signal_score}/100", market_signal_label) }
        { _metric_card("Weekly rows tracked", digest_count, "Local snapshot history with zero external hosting.") }
        { _metric_card("Completed features", feature_count, "Current product completion count in project status.") }
          { _metric_card("Setup readiness", f"{readiness_score}%", "How close the client onboarding flow is to fully self-serve.") }
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Action register</h2>
          <p>{html.escape(action_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {action_items_html}
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Meeting to execution</h2>
          <p>{html.escape(meeting_execution_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {meeting_execution_html}
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Customer health radar</h2>
          <p>{html.escape(customer_health_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {customer_health_html}
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Pipeline risk radar</h2>
          <p>{html.escape(pipeline_risk_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {pipeline_risk_html}
        </ul>
      </div>
    </section>

    <section class=\"section\">
      <div class=\"section-head\">
        <div>          <h2>Approval workflow</h2>
          <p>{html.escape(approval_workflow_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {approval_workflow_html}
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>          <h2>Briefing preview</h2>
          <p>The client-facing narrative your product produces each morning.</p>
        </div>
      </div>
      <div class=\"grid workspace\">
        <article class=\"card panel\">
          <h3>Briefing narrative</h3>
          <p>Top-level narrative extracted from the latest premium briefing.</p>
          <pre class=\"preview\">{briefing_text}</pre>
        </article>
        <aside class=\"card panel\">
          <h3>Weekly summary</h3>
          <ul class=\"summary-list\">
            <li><strong>News and market context</strong>{html.escape(str(latest_snapshot.get('news_context', 'Local briefing context is generated from live feeds and profile data.')))}</li>
            <li><strong>Trend context</strong>{html.escape(str(latest_snapshot.get('trend_context', 'Historical comparisons and anomaly detection make the product predictive.')))}</li>
            <li><strong>Enterprise coverage</strong>Slack and Microsoft 365 connectors are complete, so the system can speak to modern teams on both sides of the Google/Microsoft divide.</li>
          </ul>
        </aside>
      </div>
    </section>

    <section class=\"section\">
      <div class=\"section-head\">
        <div>
          <h2>Weekly performance</h2>
          <p>Trend table for the last generated digest.</p>
        </div>
      </div>
      <div class=\"card table-wrap\">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Completed</th>
              <th>High Open</th>
              <th>Stock Alerts</th>
              <th>Qualified</th>
              <th>Pipeline Value</th>
            </tr>
          </thead>
          <tbody>
            {digest_rows_html}
          </tbody>
        </table>
      </div>
      <div class=\"footer-note\">Weekly digest generated locally from snapshot files. No paid analytics stack required.</div>
    </section>

    <section class=\"section\">
      <div class=\"section-head\">
        <div>
          <h2>Product readiness</h2>
          <p>Customer confidence improves when the product shows its own progress.</p>
        </div>
      </div>
      <div class=\"card panel\">
        <p style=\"margin-top:0;\">The product is now positioned as a cohesive, demo-ready workflow rather than separate scripts and reports. Current components are wired for daily delivery, team context, trend awareness, and enterprise compatibility.</p>
            <p style="margin-bottom:0;"><a href="landing_page.html" target="_blank" rel="noopener">Open landing page</a> • <a href="executive_briefing.html" target="_blank" rel="noopener">Open premium briefing</a> • <a href="weekly_digest.html" target="_blank" rel="noopener">Open weekly digest</a> • <a href="client_setup_wizard.html" target="_blank" rel="noopener">Open setup wizard</a> • <a href="design_system_preview.html" target="_blank" rel="noopener">Open design system</a> • <a href="client_help_center.html" target="_blank" rel="noopener">📖 Help center</a></p>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Recommendations</h2>
          <p>{html.escape(recs_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {recs_html}
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>KPI digest</h2>
          <p>{html.escape(kpi_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">{kpi_metrics_html}</ul>
        <ul class="summary-list" style="margin-top:10px;">{kpi_flags_html}</ul>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Communication timeline</h2>
          <p>{html.escape(comm_timeline_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {timeline_html}
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Revenue forecast</h2>
          <p>{html.escape(revenue_forecast_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {revenue_forecast_html}
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Deal progression</h2>
          <p>{html.escape(deal_prog_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {deal_prog_html}
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>Renewal reminders</h2>
          <p>{html.escape(renewals_summary)}</p>
        </div>
      </div>
      <div class="card panel">
        <ul class="summary-list">
          {renewals_html}
        </ul>
      </div>
    </section>
  </main>

  <!-- 🎥 Feature tour overlay -->
  <div id="tour-overlay" style="display:none;position:fixed;inset:0;background:rgba(15,23,42,.65);z-index:9999;align-items:center;justify-content:center;">
    <div style="background:#fff;border-radius:24px;padding:36px;max-width:480px;width:90%;box-shadow:0 24px 60px rgba(15,23,42,.3);position:relative;">
      <button onclick="tourClose()" style="position:absolute;top:16px;right:20px;background:none;border:none;font-size:22px;cursor:pointer;color:#64748b;">×</button>
      <div id="tour-icon" style="font-size:40px;margin-bottom:12px;"></div>
      <h2 id="tour-title" style="margin:0 0 8px;font-size:22px;letter-spacing:-.03em;"></h2>
      <p id="tour-body" style="color:#64748b;font-size:14px;line-height:1.7;margin:0 0 24px;"></p>
      <div style="display:flex;gap:10px;justify-content:space-between;align-items:center;">
        <span id="tour-counter" style="font-size:13px;color:#94a3b8;"></span>
        <div style="display:flex;gap:8px;">
          <button id="tour-prev" onclick="tourPrev()" style="padding:10px 20px;border-radius:999px;border:1px solid #e2e8f0;background:#f8fafc;font-size:14px;cursor:pointer;">Back</button>
          <button id="tour-next" onclick="tourNext()" style="padding:10px 20px;border-radius:999px;border:none;background:#006d77;color:#fff;font-size:14px;cursor:pointer;font-weight:600;">Next</button>
        </div>
      </div>
    </div>
  </div>
  <button onclick="tourStart()" style="position:fixed;bottom:28px;right:28px;padding:14px 22px;border-radius:999px;border:none;background:#006d77;color:#fff;font-size:14px;cursor:pointer;font-weight:600;box-shadow:0 8px 24px rgba(0,109,119,.35);z-index:1000;">🎥 Product tour</button>

  <script>
  const _TOUR = [
    {{icon:'⚡',title:'Daily AI Briefing',body:'Every morning, Lucent reads your live data — tasks, CRM, emails, documents, and market feeds — and writes a concise executive briefing. Run briefing.py or use the Run Briefing shortcut.'}},
    {{icon:'🖤️',title:'Action Register',body:'All actions from tasks, email, Slack, and reply approvals are unified into one ranked list. Items scored ≥ 70/100 surface as high-priority in recommendations.'}},
    {{icon:'🔁',title:'Follow-up Autopilot',body:'Overdue tasks and stale email threads are automatically surfaced as nudge drafts. Nothing is sent without your approval — every action requires a deliberate sign-off.'}},
    {{icon:'📋',title:'Approval Workflow',body:'AI-drafted email replies queue for your review. Approve or reject each draft from the dashboard or from Slack. Approved drafts are sent via Gmail in one batch.'}},
    {{icon:'🛡️',title:'Customer Health Radar',body:'Every CRM lead is scored 0–100 using status, contact recency, deal value, and overlap with open work. Leads in the risk bucket need re-engagement today.'}},
    {{icon:'🚨',title:'Pipeline Risk Radar',body:'Active deals are ranked by slip risk based on how long they have been untouched, their value, and related open signals. Deals in the risk bucket need an escalation plan.'}},
    {{icon:'💡',title:'Recommendations Engine',body:'Powered entirely by rule-based heuristics — no extra AI call. The engine reads all live signals and suggests the 2–5 highest-impact actions for today, ranked by priority.'}},
    {{icon:'📨',title:'Email Sentiment Flagging',body:'Emails are scored as urgent, review, or routine using a weighted keyword bank. Urgent emails (score ≥ 60) are surfaced first so you never miss a critical message.'}},
    {{icon:'📈',title:'KPI Digest',body:'Up to 14 days of snapshot data are compared to detect improving, stable, or declining trends across tasks, inventory, leads, and pipeline value. Regressions are flagged before they become problems.'}},
    {{icon:'🗓️',title:'Communication Timeline',body:'All recorded touches with each customer — emails, tasks, Slack messages, CRM notes — are merged into a single ordered history. The full account picture, in one place.'}},
    {{icon:'📖',title:'Help Center',body:'Step-by-step guides for every feature, including tips and environment variable references. Open client_help_center.html at any time for a fully offline reference.'}},
  ];
  let _tourIdx = 0;
  function tourStart(){{ _tourIdx=0; _tourRender(); document.getElementById('tour-overlay').style.display='flex'; }}
  function tourClose(){{ document.getElementById('tour-overlay').style.display='none'; }}
  function tourNext(){{ if(_tourIdx < _TOUR.length-1){{ _tourIdx++; _tourRender(); }} else {{ tourClose(); }} }}
  function tourPrev(){{ if(_tourIdx > 0){{ _tourIdx--; _tourRender(); }} }}
  function _tourRender(){{
    const s = _TOUR[_tourIdx];
    document.getElementById('tour-icon').textContent = s.icon;
    document.getElementById('tour-title').textContent = s.title;
    document.getElementById('tour-body').textContent = s.body;
    document.getElementById('tour-counter').textContent = (_tourIdx+1) + ' / ' + _TOUR.length;
    document.getElementById('tour-prev').style.display = _tourIdx===0 ? 'none' : '';
    document.getElementById('tour-next').textContent = _tourIdx===_TOUR.length-1 ? 'Done' : 'Next';
  }}
  </script>
</body>
</html>
"""


def write_dashboard(path="client_dashboard.html"):
    html_content = build_dashboard_html()
    output = Path(path)
    output.write_text(html_content, encoding="utf-8")
    write_setup_wizard()
    from design_system_preview import write_design_system_preview

    write_design_system_preview()
    from landing_page import write_landing_page

    write_landing_page()
    return str(output)


if __name__ == "__main__":
    print(write_dashboard())
