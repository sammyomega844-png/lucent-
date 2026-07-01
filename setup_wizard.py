import html
import json
import os
from pathlib import Path


SOURCE_CONFIGS = [
    {
        "key": "gmail",
        "title": "Gmail",
        "env": "GMAIL_ADDRESS",
        "file": "gmail_token.json",
        "description": "Email intake for daily briefing and executive context.",
    },
    {
        "key": "notion",
        "title": "Notion",
        "env": "NOTION_TOKEN",
        "file": "credentials.json",
        "description": "Delivery target for the daily briefing archive.",
    },
    {
        "key": "slack",
        "title": "Slack",
        "env": "SLACK_BOT_TOKEN",
        "file": "slack_channels.json",
        "description": "Team decision and action-item context.",
    },
    {
        "key": "m365",
        "title": "Microsoft 365",
        "env": "M365_ACCESS_TOKEN",
        "file": "m365_config.json",
        "description": "Enterprise email, calendar, Teams, and file context.",
    },
]


def _exists(name):
    return Path(name).exists()


def _env_value(name):
    value = os.getenv(name, "").strip()
    return bool(value)


def _status_for_source(source):
    env_ok = _env_value(source["env"])
    file_ok = _exists(source["file"])
    if env_ok and file_ok:
        return "Ready", "ready"
    if env_ok or file_ok:
        return "Partially ready", "partial"
    return "Needs setup", "todo"


def _read_json(name):
    path = Path(name)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def build_setup_summary():
    sources = []
    ready_count = 0
    for source in SOURCE_CONFIGS:
        label, state = _status_for_source(source)
        if state == "ready":
            ready_count += 1
        sources.append({
            "title": source["title"],
            "description": source["description"],
            "label": label,
            "state": state,
            "env": source["env"],
            "file": source["file"],
        })

    return {
        "generated_at": "Local view",
        "readiness_score": round((ready_count / len(SOURCE_CONFIGS)) * 100),
        "ready_count": ready_count,
        "total_sources": len(SOURCE_CONFIGS),
        "sources": sources,
        "news_preferences": _read_json("news_preferences.json"),
        "slack_channels": _read_json("slack_channels.json"),
        "m365_config": _read_json("m365_config.json"),
    }


def render_setup_wizard_html(summary=None):
    summary = summary or build_setup_summary()
    source_cards = []
    for source in summary["sources"]:
        source_cards.append(
            f"""
            <article class=\"source-card {source['state']}\">
              <div class=\"source-top\">
                <div>
                  <div class=\"source-title\">{html.escape(source['title'])}</div>
                  <div class=\"source-desc\">{html.escape(source['description'])}</div>
                </div>
                <span class=\"badge\">{html.escape(source['label'])}</span>
              </div>
              <div class=\"source-meta\">Env: <code>{html.escape(source['env'])}</code> • File: <code>{html.escape(source['file'])}</code></div>
            </article>
            """
        )

    slack_channels = summary.get("slack_channels", {}).get("channels", [])
    m365_teams = summary.get("m365_config", {}).get("teams", [])
    preference_count = len(summary.get("news_preferences", {}))

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Client Setup Wizard</title>
  <style>
    :root {{
      --ink: #0f172a;
      --muted: #64748b;
      --bg: linear-gradient(135deg, #f6efe4 0%, #eef4fb 52%, #f8f8fb 100%);
      --card: rgba(255,255,255,.88);
      --border: rgba(15, 23, 42, .1);
      --good: #15803d;
      --partial: #b45309;
      --todo: #475569;
      --accent: #c2410c;
      --accent2: #0f766e;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, "Segoe UI", system-ui, -apple-system, sans-serif; color: var(--ink); background: var(--bg); }}
    .wrap {{ max-width: 1120px; margin: 0 auto; padding: 28px 16px 36px; }}
    .hero {{
      background: linear-gradient(135deg, rgba(15,23,42,.97), rgba(30,41,59,.97));
      color: #fff;
      border-radius: 28px;
      padding: 28px;
      box-shadow: 0 20px 50px rgba(15, 23, 42, .18);
      border: 1px solid rgba(255,255,255,.08);
    }}
    .eyebrow {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(255,255,255,.09);
      border: 1px solid rgba(255,255,255,.12);
      font-size: 12px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    h1 {{ margin: 12px 0 10px; font-size: clamp(30px, 4vw, 52px); line-height: .98; letter-spacing: -.04em; max-width: 12ch; }}
    .hero p {{ margin: 0; color: rgba(255,255,255,.82); max-width: 66ch; line-height: 1.6; }}
    .score-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 16px; }}
    .pill {{
      display: inline-flex;
      align-items: center;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(255,255,255,.08);
      border: 1px solid rgba(255,255,255,.12);
      font-weight: 700;
      font-size: 13px;
    }}
    .section {{ margin-top: 18px; }}
    .section-head {{ display: flex; justify-content: space-between; gap: 12px; align-items: end; margin: 22px 0 12px; }}
    .section-head h2 {{ margin: 0; font-size: 20px; letter-spacing: -.02em; }}
    .section-head p {{ margin: 0; color: var(--muted); font-size: 13px; line-height: 1.5; }}
    .grid {{ display: grid; gap: 14px; }}
    .sources {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .workspace {{ grid-template-columns: 1fr .95fr; }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 22px;
      box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
      backdrop-filter: blur(10px);
    }}
    .source-card {{ padding: 18px; }}
    .source-top {{ display: flex; justify-content: space-between; gap: 12px; align-items: start; }}
    .source-title {{ font-weight: 800; font-size: 16px; }}
    .source-desc {{ color: var(--muted); margin-top: 6px; line-height: 1.55; }}
    .source-meta {{ margin-top: 12px; color: var(--muted); font-size: 12px; }}
    .badge {{
      padding: 7px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .06em;
      background: rgba(15,23,42,.05);
      color: var(--todo);
    }}
    .ready .badge {{ color: var(--good); background: rgba(21,128,61,.08); }}
    .partial .badge {{ color: var(--partial); background: rgba(180,83,9,.08); }}
    .todo .badge {{ color: var(--todo); background: rgba(71,85,105,.08); }}
    .panel {{ padding: 18px; }}
    .panel h3 {{ margin: 0; font-size: 16px; }}
    .list {{ margin: 12px 0 0; padding-left: 18px; color: var(--muted); line-height: 1.7; }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 12px; }}
    .metric {{ padding: 16px; border-radius: 18px; border: 1px solid rgba(15,23,42,.08); background: rgba(15,23,42,.03); }}
    .metric-label {{ font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }}
    .metric-value {{ margin-top: 8px; font-size: 30px; line-height: 1; font-weight: 800; }}
    .metric-hint {{ margin-top: 6px; color: var(--muted); font-size: 13px; line-height: 1.5; }}
    .config-block {{
      margin-top: 12px;
      padding: 14px;
      border-radius: 18px;
      background: rgba(15,23,42,.03);
      border: 1px solid rgba(15,23,42,.06);
    }}
    .config-block h4 {{ margin: 0 0 8px; font-size: 14px; }}
    .config-block code {{ display: inline-block; padding: 3px 6px; border-radius: 8px; background: rgba(15,23,42,.08); }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    @media (max-width: 940px) {{
      .sources, .workspace, .summary-grid {{ grid-template-columns: 1fr; }}
      .wrap {{ padding: 18px 12px 28px; }}
      .hero {{ padding: 20px; }}
    }}
  </style>
</head>
<body>
  <main class=\"wrap\">
    <section class=\"hero\">
      <span class=\"eyebrow\">Launch Setup</span>
      <h1>Client onboarding made obvious.</h1>
      <p>This wizard shows what is ready, what still needs a token or file, and how close the platform is to a customer-ready launch. It is designed to reduce hand-holding during demos and implementation.</p>
      <div class=\"score-row\">
        <span class=\"pill\">Readiness score {summary['readiness_score']}%</span>
        <span class=\"pill\">{summary['ready_count']} of {summary['total_sources']} core sources ready</span>
        <span class=\"pill\">{preference_count} saved news topics</span>
      </div>
    </section>

    <section class=\"section\">
      <div class=\"section-head\">
        <div>
          <h2>Source readiness</h2>
          <p>Each integration is shown with its environment variable and local config file so setup is self-serve.</p>
        </div>
      </div>
      <div class=\"grid sources\">
        {''.join(source_cards)}
      </div>
    </section>

    <section class=\"section\">
      <div class=\"section-head\">
        <div>
          <h2>What the client can do next</h2>
          <p>These are the actions that make the product look and feel professionally packaged.</p>
        </div>
      </div>
      <div class=\"grid workspace\">
        <article class=\"card panel\">
          <h3>Recommended onboarding flow</h3>
          <ol class=\"list\">
            <li>Set the environment variables for the sources you want to enable.</li>
            <li>Drop in or generate the local config files for Slack and Microsoft 365.</li>
            <li>Run the briefing once to produce a premium briefing plus dashboard.</li>
            <li>Share the dashboard and setup wizard with the customer for approval.</li>
            <li>Use the weekly digest and dashboard to prove trend tracking and execution quality.</li>
          </ol>
        </article>
        <aside class=\"card panel\">
          <h3>Current configuration signals</h3>
          <div class=\"config-block\">
            <h4>Slack channels</h4>
            <div>{html.escape(', '.join(slack_channels) if slack_channels else 'No Slack channels configured yet.')}</div>
          </div>
          <div class="config-block">
            <h4>Microsoft 365 setup checklist</h4>
            <ol class="list" style="margin-top:6px; padding-left:18px;">
              <li>Create an Azure app registration in Microsoft Entra ID.</li>
              <li>Grant and consent Graph scopes: Mail.Read, Calendars.Read, Files.Read, ChannelMessage.Read.All.</li>
              <li>Set <code>M365_ACCESS_TOKEN</code> and create <code>m365_config.json</code> for Teams channels.</li>
              <li>Run one briefing and verify Microsoft data appears in dashboard context.</li>
            </ol>
          </div>
          <div class=\"config-block\">
            <h4>Microsoft 365 teams</h4>
            <div>{html.escape(', '.join(str(item.get('channel_id', 'unknown')) for item in m365_teams) if m365_teams else 'No Teams channels configured yet.')}</div>
          </div>
          <div class=\"config-block\">
            <h4>Integration note</h4>
            <div>Everything here stays local and free until you choose to connect a customer environment.</div>
          </div>
        </aside>
      </div>
    </section>

    <section class=\"section\">
      <div class=\"section-head\">
        <div>
          <h2>Launch signals</h2>
          <p>Short version: enough polish exists to demo, but the wizard makes onboarding repeatable.</p>
        </div>
      </div>
      <div class=\"summary-grid\">
        <article class=\"card metric\">
          <div class=\"metric-label\">Ready integrations</div>
          <div class=\"metric-value\">{summary['ready_count']}</div>
          <div class=\"metric-hint\">Core sources already configured or partially in place.</div>
        </article>
        <article class=\"card metric\">
          <div class=\"metric-label\">Setup friction</div>
          <div class=\"metric-value\">Low</div>
          <div class=\"metric-hint\">Customer-friendly instructions and visible readiness markers.</div>
        </article>
        <article class=\"card metric\">
          <div class=\"metric-label\">Launch posture</div>
          <div class=\"metric-value\">Ready</div>
          <div class=\"metric-hint\">Good enough to present, pilot, and iterate in front of customers.</div>
        </article>
      </div>
      <div class=\"config-block\" style=\"margin-top:14px;\">
          <strong>Next open files:</strong> <a href=\"client_dashboard.html\" target=\"_blank\" rel=\"noopener\">client_dashboard.html</a> · <a href=\"executive_briefing.html\" target=\"_blank\" rel=\"noopener\">executive_briefing.html</a> · <a href=\"weekly_digest.html\" target=\"_blank\" rel=\"noopener\">weekly_digest.html</a>
      </div>
    </section>
  </main>
</body>
</html>
"""


def write_setup_wizard(output_html="client_setup_wizard.html", output_json="client_setup_wizard.json"):
    summary = build_setup_summary()
    Path(output_html).write_text(render_setup_wizard_html(summary), encoding="utf-8")
    Path(output_json).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return output_html, output_json


if __name__ == "__main__":
    html_path, json_path = write_setup_wizard()
    print(f"Generated {html_path} and {json_path}")
