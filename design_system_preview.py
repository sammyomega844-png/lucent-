from pathlib import Path

from design_system import TOKENS, write_design_system_css


def _swatch(name, value):
    return (
        "<article class=\"ds-card\">"
        f"<div class=\"ds-title-md\">{name}</div>"
        f"<div style=\"margin-top:10px;height:42px;border-radius:10px;border:1px solid var(--ds-border);background:{value};\"></div>"
        f"<p class=\"ds-text ds-muted\" style=\"margin-top:8px;\">{value}</p>"
        "</article>"
    )


def build_design_system_preview_html():
    write_design_system_css()
    swatches = []
    for name, value in TOKENS["color"].items():
        swatches.append(_swatch(name, value))

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Design System Preview</title>
  <link rel=\"stylesheet\" href=\"design_system.css\">
</head>
<body>
  <main class=\"ds-shell ds-stack\">
    <section class=\"ds-card hero ds-stack\">
      <span class="ds-eyebrow">Lucent Design System</span>
      <h1 class=\"ds-title-xl\">A cohesive visual language for every customer touchpoint.</h1>
      <p class=\"ds-text\">This preview defines the foundational tokens and reusable components that power landing pages, dashboards, setup flows, and future authenticated app screens.</p>
      <div class=\"ds-button-row\">
        <button class=\"ds-btn primary\">Primary action</button>
        <button class=\"ds-btn secondary\">Secondary action</button>
        <button class=\"ds-btn ghost\">Ghost action</button>
      </div>
    </section>

    <section class=\"ds-stack\">
      <h2 class=\"ds-title-lg\">Color tokens</h2>
      <div class=\"ds-grid cols-4\">{''.join(swatches)}</div>
    </section>

    <section class=\"ds-stack\">
      <h2 class=\"ds-title-lg\">KPI cards</h2>
      <div class=\"ds-grid cols-4\">
        <article class=\"ds-kpi\">
          <div class=\"ds-kpi-label\">Setup readiness</div>
          <div class=\"ds-kpi-value\">84%</div>
          <div class=\"ds-kpi-hint\">Share this in demos to show implementation maturity.</div>
        </article>
        <article class=\"ds-kpi\">
          <div class=\"ds-kpi-label\">Daily briefings</div>
          <div class=\"ds-kpi-value\">100%</div>
          <div class=\"ds-kpi-hint\">Consistent briefing delivery across customer pilots.</div>
        </article>
        <article class=\"ds-kpi\">
          <div class=\"ds-kpi-label\">Trend coverage</div>
          <div class=\"ds-kpi-value\">14d</div>
          <div class=\"ds-kpi-hint\">Built-in historical awareness from local snapshots.</div>
        </article>
        <article class=\"ds-kpi\">
          <div class=\"ds-kpi-label\">Cost model</div>
          <div class=\"ds-kpi-value\">Free tier</div>
          <div class=\"ds-kpi-hint\">No required paid dependency for launch-ready demos.</div>
        </article>
      </div>
    </section>

    <section class=\"ds-grid cols-2\">
      <article class=\"ds-card ds-stack\">
        <h3 class=\"ds-title-md\">Form controls</h3>
        <div>
          <label class=\"ds-label\">Client email</label>
          <input class=\"ds-input\" placeholder=\"name@company.com\">
        </div>
        <div>
          <label class=\"ds-label\">Primary stack</label>
          <select class=\"ds-select\">
            <option>Google Workspace</option>
            <option>Microsoft 365</option>
            <option>Hybrid</option>
          </select>
        </div>
        <div>
          <label class=\"ds-label\">Notes</label>
          <textarea class=\"ds-textarea\" rows=\"4\" placeholder=\"Add onboarding context\"></textarea>
        </div>
      </article>

      <article class=\"ds-card ds-stack\">
        <h3 class=\"ds-title-md\">Status badges</h3>
        <p class=\"ds-text\">Use badge tones consistently across all pages.</p>
        <div class=\"ds-button-row\">
          <span class=\"ds-tag good\">Ready</span>
          <span class=\"ds-tag watch\">In progress</span>
          <span class=\"ds-tag risk\">Needs input</span>
        </div>
      </article>
    </section>
  </main>
</body>
</html>
"""


def write_design_system_preview(path="design_system_preview.html"):
    output = Path(path)
    output.write_text(build_design_system_preview_html(), encoding="utf-8")
    return str(output)


if __name__ == "__main__":
    print(write_design_system_preview())
