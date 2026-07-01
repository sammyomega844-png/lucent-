import html
from pathlib import Path


def _score_class(score):
    if score >= 80:
        return "good"
    if score >= 60:
        return "watch"
    return "risk"


def render_premium_report(
    *,
    today,
    loaded_at,
    overall_score,
    day_rating,
    market_signal_score,
    market_signal_label,
    news_context,
    roadmap_summary,
    briefing,
    one_click_feedback_links=None,
):
    """Return a standalone premium-style HTML report from briefing content."""
    one_click_feedback_links = one_click_feedback_links or []
    score_class = _score_class(int(overall_score))
    digest_path = Path("weekly_digest.html")
    if digest_path.exists():
        digest_html = (
            '<section class="panel digest">'
            '<h3>Weekly Digest</h3>'
            '<p>Your weekly executive trend digest is ready.</p>'
            '<p><a href="weekly_digest.html" target="_blank" rel="noopener">Open weekly_digest.html</a></p>'
            "</section>"
        )
    else:
        digest_html = (
            '<section class="panel digest">'
            '<h3>Weekly Digest</h3>'
            '<p>Weekly digest not generated yet. Run weekly_digest.py to create it.</p>'
            "</section>"
        )
    feedback_html = ""
    if one_click_feedback_links:
        rows = []
        for topic, url in one_click_feedback_links:
            rows.append(
                f'<li><a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">'
                f'Upvote {html.escape(topic)}</a></li>'
            )
        feedback_html = (
            "<section class=\"panel\"><h3>One-Click Feedback</h3>"
            "<ul class=\"feedback\">"
            + "".join(rows)
            + "</ul></section>"
        )

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Executive Briefing Report</title>
  <style>
    :root {{
      --ink: #0e1f31;
      --card: #f7f7f2;
      --bg: linear-gradient(135deg, #f0ede3 0%, #dbe7f2 45%, #f4f0e8 100%);
      --accent: #bb3e03;
      --good: #2a9d8f;
      --watch: #e9c46a;
      --risk: #ae2012;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, Cambria, "Times New Roman", serif;
      color: var(--ink);
      background: var(--bg);
      min-height: 100vh;
      padding: 28px 14px;
    }}
    .wrap {{ max-width: 980px; margin: 0 auto; }}
    .hero {{
      background: #102a43;
      color: #f8f7f3;
      border-radius: 18px;
      padding: 24px;
      box-shadow: 0 12px 28px rgba(16, 42, 67, 0.22);
    }}
    .title {{ margin: 0; font-size: 30px; line-height: 1.15; letter-spacing: 0.2px; }}
    .sub {{ margin-top: 8px; opacity: 0.9; font-size: 15px; }}
    .chips {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 14px; }}
    .chip {{
      padding: 8px 12px;
      border-radius: 999px;
      font-size: 13px;
      background: rgba(248, 247, 243, 0.12);
      border: 1px solid rgba(248, 247, 243, 0.25);
    }}
    .chip.good {{ border-color: var(--good); }}
    .chip.watch {{ border-color: var(--watch); }}
    .chip.risk {{ border-color: var(--risk); }}
    .grid {{ display: grid; grid-template-columns: repeat(12, 1fr); gap: 14px; margin-top: 14px; }}
    .panel {{
      background: var(--card);
      border: 1px solid rgba(16, 42, 67, 0.12);
      border-radius: 16px;
      padding: 16px;
      box-shadow: 0 6px 18px rgba(16, 42, 67, 0.08);
    }}
    .panel h3 {{ margin: 0 0 10px; font-size: 18px; }}
    .meta {{ grid-column: span 4; }}
    .roadmap {{ grid-column: span 8; }}
    .digest {{ grid-column: span 6; }}
    .briefing {{ grid-column: span 12; }}
    .feedback li {{ margin-bottom: 6px; }}
    .briefing pre {{ white-space: pre-wrap; font-family: inherit; font-size: 16px; line-height: 1.55; margin: 0; }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    @media (max-width: 860px) {{
      .meta, .roadmap, .briefing {{ grid-column: span 12; }}
      .title {{ font-size: 26px; }}
    }}
  </style>
</head>
<body>
  <main class=\"wrap\">
    <section class=\"hero\">
      <h1 class=\"title\">Executive Morning Briefing</h1>
      <div class=\"sub\">{html.escape(str(today))} • Refreshed at {html.escape(str(loaded_at))}</div>
      <div class=\"chips\">
        <span class=\"chip {score_class}\">Day Score: {html.escape(str(overall_score))}/100</span>
        <span class=\"chip\">Rating: {html.escape(str(day_rating))}</span>
        <span class=\"chip\">Strategic Pulse: {html.escape(str(market_signal_score))}/100</span>
        <span class=\"chip\">Signal: {html.escape(str(market_signal_label))}</span>
      </div>
    </section>

    <section class=\"grid\">
      <article class=\"panel meta\">
        <h3>News Context</h3>
        <p>{html.escape(str(news_context))}</p>
      </article>

      <article class=\"panel roadmap\">
        <h3>Roadmap Snapshot</h3>
        <pre>{html.escape(str(roadmap_summary))}</pre>
      </article>

      <article class=\"panel briefing\">
        <h3>Briefing Narrative</h3>
        <pre>{html.escape(str(briefing))}</pre>
      </article>
      {feedback_html}
      {digest_html}
    </section>
  </main>
</body>
</html>
"""


def write_premium_report(path, **kwargs):
    """Render and write the premium HTML report to disk."""
    html_content = render_premium_report(**kwargs)
    output = Path(path)
    output.write_text(html_content, encoding="utf-8")
    return str(output)
