"""
Help Center — generates a static HTML help page with per-feature
step-by-step guides. No external dependencies.
"""

import html as _html
from pathlib import Path

OUTPUT_FILE = "client_help_center.html"


_FEATURES = [
    {
        "id": "daily-briefing",
        "icon": "⚡",
        "title": "Daily AI Briefing",
        "summary": "Your personalised executive briefing, generated every morning from live data.",
        "steps": [
            "Ensure your data sources (Gmail, tasks, CRM) are connected via the Setup Wizard.",
            "Run <code>briefing.py</code> each morning (or schedule it via the Run Briefing shortcut).",
            "The briefing is written to <code>executive_briefing.html</code> and appears in the dashboard preview.",
            "Each section (News, Risk & Opportunity, Action Register, etc.) is populated from your live data.",
            "Adjust the <code>QUICK_REPLY_ENABLED</code> environment variable to enable draft email suggestions.",
        ],
        "tips": [
            "Set <code>OLLAMA_MODEL</code> or <code>OPENAI_API_KEY</code> in <code>.env</code> to choose your AI model.",
            "The briefing stays under 450 words by design — it is built for executives, not analysts.",
        ],
    },
    {
        "id": "action-register",
        "icon": "🗂️",
        "title": "Action Register",
        "summary": "A unified, ranked list of the most important actions from tasks, email, and Slack.",
        "steps": [
            "The action register is generated automatically each time the briefing runs.",
            "Items are ranked by score (0–100) based on priority, source, and urgency keywords.",
            "View the register in the <strong>Action register</strong> section of the dashboard.",
            "The register file is saved to <code>action_register.json</code> in the project folder.",
        ],
        "tips": [
            "Items with a score ≥ 70 are treated as high-priority in the recommendations engine.",
            "Slack items appear if <code>SLACK_BOT_TOKEN</code> and at least one channel ID are configured.",
        ],
    },
    {
        "id": "follow-up-autopilot",
        "icon": "🔁",
        "title": "Follow-up Autopilot",
        "summary": "Automatically surfaces overdue tasks and stale email threads that need a nudge.",
        "steps": [
            "Follow-up items are built from overdue tasks, pending reply approvals, and stale action register items.",
            "Each item includes a suggested nudge subject and body ready to send.",
            "View the list in the <strong>Follow-up autopilot</strong> section of the dashboard.",
            "To act on a nudge, copy the suggested message and send it from your email client.",
        ],
        "tips": [
            "Items involving reply approvals also appear in the Approval Workflow section.",
            "The autopilot does not send anything automatically — all sends require your approval.",
        ],
    },
    {
        "id": "approval-workflow",
        "icon": "📋",
        "title": "Approval Workflow",
        "summary": "Review and approve AI-drafted email replies before they are sent.",
        "steps": [
            "Enable draft generation by setting <code>QUICK_REPLY_ENABLED=1</code> in your <code>.env</code> file.",
            "Each run, the briefing creates draft replies for emails that match action keywords.",
            "Drafts appear in the <strong>Approval workflow</strong> section of the dashboard.",
            "To approve a draft programmatically, call <code>approve_draft_in_workflow(draft_id)</code>.",
            "Once approved, call <code>send_workflow_approved_drafts()</code> to send via Gmail.",
            "If Slack is configured, pending drafts are also posted to <code>SLACK_APPROVAL_CHANNEL</code>.",
        ],
        "tips": [
            "Rejected drafts are logged in <code>response_audit_log.jsonl</code> for review.",
            "Set <code>QUICK_REPLY_MAX_DRAFTS</code> to limit how many drafts are created per run.",
        ],
    },
    {
        "id": "customer-health",
        "icon": "🛡️",
        "title": "Customer Health Radar",
        "summary": "Scores each CRM lead by health — healthy, watch, or at risk — using multiple signals.",
        "steps": [
            "The radar reads your <code>crm.csv</code> file and scores each lead out of 100.",
            "Scoring uses: CRM status, last contact recency, deal value, and overlap with open work items.",
            "View scores in the <strong>Customer health radar</strong> section of the dashboard.",
            "Leads in the <em>risk</em> bucket should be re-engaged before they go cold.",
            "The report is saved to <code>customer_health_report.json</code>.",
        ],
        "tips": [
            "Update <code>Last_Contact</code> in your CRM after every customer touchpoint for accurate scoring.",
            "Leads with many open action or follow-up items get a penalty — resolve open work to improve scores.",
        ],
    },
    {
        "id": "pipeline-risk",
        "icon": "🚨",
        "title": "Pipeline Risk Radar",
        "summary": "Flags active deals most likely to slip based on staleness, value, and open signals.",
        "steps": [
            "The pipeline risk radar runs automatically as part of the briefing.",
            "Active deals (not Lost) are scored on staleness, value, and related open work signals.",
            "Deals in the <em>risk</em> bucket need immediate escalation.",
            "View the ranked list in the <strong>Pipeline risk radar</strong> section of the dashboard.",
        ],
        "tips": [
            "A deal that has gone untouched for 30+ days automatically increases its risk score.",
            "Adding the company name to task names or Slack messages helps the radar detect related signals.",
        ],
    },
    {
        "id": "recommendations",
        "icon": "💡",
        "title": "Recommendations Engine",
        "summary": "Smart, pattern-based suggestions generated from all live signals — no AI call needed.",
        "steps": [
            "Recommendations are built automatically each time the briefing runs.",
            "The engine reads the action register, follow-up plan, customer health, pipeline risk, and KPI digest.",
            "Each recommendation includes a rationale, priority (high/medium), and a clear action step.",
            "View recommendations in the dashboard's <strong>Recommendations</strong> section.",
        ],
        "tips": [
            "High-priority recommendations appear first and are surfaced in the briefing prompt.",
            "The engine is fully offline — it uses rule-based heuristics, not a language model.",
        ],
    },
    {
        "id": "kpi-digest",
        "icon": "📈",
        "title": "KPI Performance Digest",
        "summary": "Tracks key business metrics across snapshots and flags trends before they become problems.",
        "steps": [
            "The KPI digest reads up to 14 days of daily snapshot files.",
            "It computes trends for: completed tasks, overdue tasks, stock alerts, qualified leads, and pipeline value.",
            "KPIs trending in the wrong direction are flagged in the <strong>KPI flags</strong> list.",
            "View the digest in the <strong>KPI digest</strong> section of the dashboard.",
        ],
        "tips": [
            "Snapshot files must be named <code>snapshot_YYYY-MM-DD.json</code> to be picked up automatically.",
            "Run <code>update.py</code> daily to generate fresh snapshots.",
        ],
    },
    {
        "id": "communication-timeline",
        "icon": "🗓️",
        "title": "Customer Communication Timeline",
        "summary": "A per-account history of all recorded touches: emails, tasks, Slack messages, and CRM notes.",
        "steps": [
            "The timeline is built from CRM rows matched against emails, tasks, and Slack messages.",
            "Each account shows up to 8 most-recent touches sorted by date.",
            "View timelines in the <strong>Communication timeline</strong> section of the dashboard.",
            "The report is saved to <code>communication_timeline.json</code>.",
        ],
        "tips": [
            "Mention the company name in task names and Slack messages for better matching.",
            "The timeline is local — no data leaves your machine.",
        ],
    },
    {
        "id": "email-sentiment",
        "icon": "📬",
        "title": "Email Sentiment Flagging",
        "summary": "Automatically scores emails as urgent, review, or routine so you know what to read first.",
        "steps": [
            "Emails fetched during the briefing are automatically scored using keyword signals.",
            "Urgent emails (score ≥ 60/100) are surfaced first in the sentiment report.",
            "View the flagged list in the <strong>Email sentiment</strong> section of the dashboard.",
            "No AI call is needed — the scorer uses a weighted keyword bank.",
        ],
        "tips": [
            "The baseline score is 30 — any action or urgency keyword raises it above the 60-point urgent threshold.",
            "Newsletter and digest keywords reduce the score, keeping routine mail from cluttering the urgent queue.",
        ],
    },
    {
        "id": "setup-wizard",
        "icon": "🧭",
        "title": "Setup Wizard",
        "summary": "Self-serve onboarding that checks which data sources are connected and guides first-time setup.",
        "steps": [
            "Open <code>client_setup_wizard.html</code> or run <code>setup_wizard.py</code>.",
            "Each source shows a status badge: Connected, Needs setup, or Optional.",
            "Follow the checklist for each source to connect Gmail, Slack, Microsoft 365, or Notion.",
            "The readiness score updates as more sources are connected.",
        ],
        "tips": [
            "Microsoft 365 uses <code>M365_ACCESS_TOKEN</code> — generate this via the Microsoft Graph Explorer for free.",
            "Notion integration uses <code>NOTION_API_KEY</code> and <code>NOTION_PAGE_ID</code> from your Notion settings.",
        ],
    },
]


def _feature_section(feature):
    fid = _html.escape(feature["id"])
    icon = feature["icon"]
    title = _html.escape(feature["title"])
    summary = _html.escape(feature["summary"])

    steps_html = "".join(
        f'<li>{step}</li>'
        for step in feature["steps"]
    )
    tips_html = "".join(
        f'<li>{tip}</li>'
        for tip in feature.get("tips", [])
    )
    tips_block = (
        f'<div class="tips"><strong>Tips</strong><ul>{tips_html}</ul></div>'
        if tips_html else ""
    )

    return f"""
    <section class="feature" id="{fid}">
      <div class="feature-header">
        <span class="feature-icon">{icon}</span>
        <div>
          <h2>{title}</h2>
          <p class="feature-summary">{summary}</p>
        </div>
      </div>
      <ol class="steps">{steps_html}</ol>
      {tips_block}
    </section>"""


def _nav_item(feature):
    fid = _html.escape(feature["id"])
    icon = feature["icon"]
    title = _html.escape(feature["title"])
    return f'<li><a href="#{fid}">{icon} {title}</a></li>'


def build_help_center_html():
    nav = "".join(_nav_item(f) for f in _FEATURES)
    sections = "".join(_feature_section(f) for f in _FEATURES)
    from datetime import date
    today = date.today().isoformat()

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lucent — Help Center</title>
  <style>
    :root {{
      --ink: #12263a;
      --muted: #64748b;
      --bg: #f8fafc;
      --card: #ffffff;
      --border: #e2e8f0;
      --accent: #006d77;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, "Segoe UI", system-ui, sans-serif; color: var(--ink); background: var(--bg); }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .layout {{ display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }}
    .sidebar {{
      background: var(--card);
      border-right: 1px solid var(--border);
      padding: 28px 20px;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
    }}
    .sidebar .logo {{ font-size: 22px; font-weight: 800; letter-spacing: -.04em; color: var(--ink); margin-bottom: 8px; }}
    .sidebar .tagline {{ font-size: 12px; color: var(--muted); margin-bottom: 24px; }}
    .sidebar nav ul {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 4px; }}
    .sidebar nav li a {{
      display: block;
      padding: 8px 12px;
      border-radius: 10px;
      font-size: 14px;
      color: var(--ink);
      transition: background .15s;
    }}
    .sidebar nav li a:hover {{ background: #f1f5f9; text-decoration: none; }}
    .content {{ padding: 40px 48px; max-width: 820px; }}
    .page-title {{ font-size: 32px; font-weight: 800; letter-spacing: -.04em; margin: 0 0 8px; }}
    .page-sub {{ color: var(--muted); font-size: 15px; margin: 0 0 40px; }}
    .feature {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 28px;
      margin-bottom: 24px;
      scroll-margin-top: 32px;
    }}
    .feature-header {{ display: flex; gap: 16px; align-items: flex-start; margin-bottom: 20px; }}
    .feature-icon {{ font-size: 32px; flex-shrink: 0; }}
    .feature-header h2 {{ margin: 0; font-size: 20px; letter-spacing: -.02em; }}
    .feature-summary {{ color: var(--muted); font-size: 14px; margin: 4px 0 0; }}
    .steps {{ padding-left: 20px; margin: 0 0 16px; display: grid; gap: 10px; }}
    .steps li {{ font-size: 14px; line-height: 1.7; }}
    .tips {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 14px 18px; }}
    .tips strong {{ font-size: 13px; color: #166534; }}
    .tips ul {{ margin: 8px 0 0; padding-left: 18px; display: grid; gap: 6px; }}
    .tips li {{ font-size: 13px; color: #166534; line-height: 1.6; }}
    code {{ background: #f1f5f9; border: 1px solid var(--border); border-radius: 5px; padding: 2px 6px; font-size: 13px; font-family: "Fira Code", Consolas, monospace; }}
    .footer {{ color: var(--muted); font-size: 12px; margin-top: 48px; padding-top: 20px; border-top: 1px solid var(--border); }}
    @media (max-width: 860px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{ position: static; height: auto; border-right: none; border-bottom: 1px solid var(--border); }}
      .content {{ padding: 24px 20px; }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <div class="logo">Lucent</div>
      <div class="tagline">Help Center</div>
      <nav><ul>{nav}</ul></nav>
    </aside>
    <main class="content">
      <h1 class="page-title">Help Center</h1>
      <p class="page-sub">Step-by-step guides for every Lucent feature. Updated {today}.</p>
      {sections}
      <div class="footer">Lucent Help Center — generated locally. No data leaves your machine.</div>
    </main>
  </div>
</body>
</html>"""


def write_help_center(path=OUTPUT_FILE):
    content = build_help_center_html()
    Path(path).write_text(content, encoding="utf-8")
    return path


if __name__ == "__main__":
    out = write_help_center()
    print(out)
