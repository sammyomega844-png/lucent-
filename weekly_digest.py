import json
import os
from datetime import date, datetime, timedelta
from pathlib import Path

from status_sync import update_project_status
from dashboard import write_dashboard


def _load_snapshot(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None


def _snapshot_metrics(snapshot):
    tasks = snapshot.get("tasks", {})
    inventory = snapshot.get("inventory", {})
    crm = snapshot.get("crm", {})

    completed = 0
    high_open = 0
    for task in tasks.values():
        if task.get("status") == "Completed":
            completed += 1
        if task.get("priority") == "High" and task.get("status") != "Completed":
            high_open += 1

    stock_alerts = 0
    for item in inventory.values():
        try:
            if int(item.get("stock", 0)) < int(item.get("reorder", 0)):
                stock_alerts += 1
        except Exception:
            continue

    qualified = 0
    pipeline_value = 0.0
    for lead in crm.values():
        if lead.get("status") == "Qualified":
            qualified += 1
        try:
            if lead.get("status") != "Lost":
                pipeline_value += float(lead.get("value", 0))
        except Exception:
            continue

    return {
        "completed": completed,
        "high_open": high_open,
        "stock_alerts": stock_alerts,
        "qualified": qualified,
        "pipeline_value": round(pipeline_value, 2),
    }


def build_weekly_digest(days=7):
    today = date.today()
    rows = []
    for offset in range(days - 1, -1, -1):
        day = today - timedelta(days=offset)
        snapshot_path = Path(f"snapshot_{day.isoformat()}.json")
        if not snapshot_path.exists():
            continue
        snapshot = _load_snapshot(snapshot_path)
        if not snapshot:
            continue
        metrics = _snapshot_metrics(snapshot)
        metrics["date"] = day.isoformat()
        rows.append(metrics)

    if not rows:
        return {
            "generated_at": datetime.now().isoformat(),
            "days": [],
            "summary": {
                "avg_completed": 0,
                "avg_high_open": 0,
                "avg_stock_alerts": 0,
                "avg_qualified": 0,
                "avg_pipeline_value": 0,
            },
        }

    count = len(rows)
    summary = {
        "avg_completed": round(sum(r["completed"] for r in rows) / count, 1),
        "avg_high_open": round(sum(r["high_open"] for r in rows) / count, 1),
        "avg_stock_alerts": round(sum(r["stock_alerts"] for r in rows) / count, 1),
        "avg_qualified": round(sum(r["qualified"] for r in rows) / count, 1),
        "avg_pipeline_value": round(sum(r["pipeline_value"] for r in rows) / count, 2),
    }

    return {
        "generated_at": datetime.now().isoformat(),
        "days": rows,
        "summary": summary,
    }


def render_weekly_digest_html(digest):
    rows_html = ""
    for row in digest.get("days", []):
        rows_html += (
            f"<tr><td>{row['date']}</td>"
            f"<td>{row['completed']}</td>"
            f"<td>{row['high_open']}</td>"
            f"<td>{row['stock_alerts']}</td>"
            f"<td>{row['qualified']}</td>"
            f"<td>${row['pipeline_value']:,.0f}</td></tr>"
        )

    s = digest.get("summary", {})
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Weekly Executive Digest</title>
  <style>
    :root {{
      --bg: linear-gradient(120deg, #f8f4ec 0%, #eaf2f7 100%);
      --ink: #12263a;
      --card: #ffffff;
      --accent: #006d77;
      --accent2: #bb3e03;
    }}
    body {{ margin: 0; font-family: "Segoe UI", Tahoma, sans-serif; color: var(--ink); background: var(--bg); padding: 24px 14px; }}
    .wrap {{ max-width: 980px; margin: 0 auto; }}
    .hero {{ background: #102a43; color: #fff; border-radius: 16px; padding: 22px; }}
    .hero h1 {{ margin: 0; font-size: 28px; }}
    .hero p {{ margin: 6px 0 0; opacity: 0.9; }}
    .cards {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 14px; }}
    .card {{ background: var(--card); border: 1px solid #dce6ef; border-radius: 12px; padding: 12px; box-shadow: 0 4px 12px rgba(16, 42, 67, 0.08); }}
    .label {{ font-size: 12px; color: #4a6072; }}
    .value {{ font-size: 24px; font-weight: 700; color: var(--accent); margin-top: 4px; }}
    .table {{ margin-top: 14px; background: var(--card); border: 1px solid #dce6ef; border-radius: 12px; overflow: hidden; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 10px 12px; text-align: left; font-size: 14px; border-bottom: 1px solid #eef3f7; }}
    th {{ background: #f3f8fc; font-weight: 700; }}
    tr:last-child td {{ border-bottom: none; }}
    .note {{ margin-top: 10px; font-size: 13px; color: #4a6072; }}
    @media (max-width: 900px) {{
      .cards {{ grid-template-columns: repeat(2, 1fr); }}
    }}
  </style>
</head>
<body>
  <main class=\"wrap\">
    <section class=\"hero\">
      <h1>Weekly Executive Digest</h1>
      <p>Generated at {digest.get('generated_at', '')}</p>
    </section>

    <section class=\"cards\">
      <article class=\"card\"><div class=\"label\">Avg Completed</div><div class=\"value\">{s.get('avg_completed', 0)}</div></article>
      <article class=\"card\"><div class=\"label\">Avg High Priority Open</div><div class=\"value\">{s.get('avg_high_open', 0)}</div></article>
      <article class=\"card\"><div class=\"label\">Avg Stock Alerts</div><div class=\"value\">{s.get('avg_stock_alerts', 0)}</div></article>
      <article class=\"card\"><div class=\"label\">Avg Qualified Leads</div><div class=\"value\">{s.get('avg_qualified', 0)}</div></article>
      <article class=\"card\"><div class=\"label\">Avg Pipeline Value</div><div class=\"value\">${s.get('avg_pipeline_value', 0):,.0f}</div></article>
    </section>

    <section class=\"table\">
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
          {rows_html}
        </tbody>
      </table>
    </section>

    <div class=\"note\">This digest uses local snapshot files only, so it adds zero new paid dependencies.</div>
  </main>
</body>
</html>
"""


def write_weekly_digest(output_html="weekly_digest.html", output_json="weekly_digest.json", days=7):
    digest = build_weekly_digest(days=days)
    html_text = render_weekly_digest_html(digest)
    Path(output_html).write_text(html_text, encoding="utf-8")
    Path(output_json).write_text(json.dumps(digest, indent=2), encoding="utf-8")
    return output_html, output_json


def main():
    days = int(os.getenv("WEEKLY_DIGEST_DAYS", "7"))
    html_out, json_out = write_weekly_digest(days=days)
    update_project_status(source="weekly digest")
    dashboard_path = write_dashboard()
    print(f"Customer dashboard refreshed: {dashboard_path}")
    print(f"Weekly digest generated: {html_out}, {json_out}")


if __name__ == "__main__":
    main()
