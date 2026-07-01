from pathlib import Path


TOKENS = {
    "color": {
        "ink": "#0f172a",
        "ink_soft": "#334155",
        "muted": "#64748b",
        "bg": "#f8fafc",
        "surface": "#ffffff",
        "surface_alt": "#f1f5f9",
        "border": "rgba(15, 23, 42, 0.12)",
        "brand": "#c2410c",
        "brand_alt": "#0f766e",
        "brand_cool": "#1d4ed8",
        "good": "#15803d",
        "watch": "#b45309",
        "risk": "#b91c1c",
    },
    "radius": {
        "sm": "10px",
        "md": "16px",
        "lg": "24px",
        "pill": "999px",
    },
    "space": {
        "xs": "6px",
        "sm": "10px",
        "md": "14px",
        "lg": "18px",
        "xl": "24px",
        "xxl": "32px",
    },
}


def build_design_system_css():
    c = TOKENS["color"]
    r = TOKENS["radius"]
    s = TOKENS["space"]

    return f"""
:root {{
  --ds-ink: {c['ink']};
  --ds-ink-soft: {c['ink_soft']};
  --ds-muted: {c['muted']};
  --ds-bg: {c['bg']};
  --ds-surface: {c['surface']};
  --ds-surface-alt: {c['surface_alt']};
  --ds-border: {c['border']};
  --ds-brand: {c['brand']};
  --ds-brand-alt: {c['brand_alt']};
  --ds-brand-cool: {c['brand_cool']};
  --ds-good: {c['good']};
  --ds-watch: {c['watch']};
  --ds-risk: {c['risk']};
  --ds-r-sm: {r['sm']};
  --ds-r-md: {r['md']};
  --ds-r-lg: {r['lg']};
  --ds-r-pill: {r['pill']};
  --ds-sp-xs: {s['xs']};
  --ds-sp-sm: {s['sm']};
  --ds-sp-md: {s['md']};
  --ds-sp-lg: {s['lg']};
  --ds-sp-xl: {s['xl']};
  --ds-sp-xxl: {s['xxl']};
  --ds-shadow-sm: 0 6px 16px rgba(15, 23, 42, 0.06);
  --ds-shadow-md: 0 14px 28px rgba(15, 23, 42, 0.09);
}}

* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  color: var(--ds-ink);
  background: linear-gradient(135deg, #f7efe4 0%, #edf4fb 52%, #f9fafc 100%);
  font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
}}

a {{ color: var(--ds-brand); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

.ds-shell {{ max-width: 1160px; margin: 0 auto; padding: var(--ds-sp-xxl) var(--ds-sp-lg); }}
.ds-stack {{ display: grid; gap: var(--ds-sp-lg); }}
.ds-grid {{ display: grid; gap: var(--ds-sp-md); }}
.ds-grid.cols-2 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
.ds-grid.cols-3 {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
.ds-grid.cols-4 {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}

.ds-card {{
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-r-md);
  background: var(--ds-surface);
  box-shadow: var(--ds-shadow-sm);
  padding: var(--ds-sp-lg);
}}
.ds-card.hero {{
  border-radius: var(--ds-r-lg);
  background: linear-gradient(135deg, rgba(15,23,42,.97), rgba(30,41,59,.97));
  color: #fff;
  box-shadow: var(--ds-shadow-md);
}}

.ds-eyebrow {{
  display: inline-flex;
  align-items: center;
  gap: var(--ds-sp-xs);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border-radius: var(--ds-r-pill);
  padding: 8px 12px;
  border: 1px solid rgba(255,255,255,0.22);
  background: rgba(255,255,255,0.10);
}}

.ds-title-xl {{ margin: 8px 0 6px; font-size: clamp(34px, 5vw, 56px); line-height: 0.95; letter-spacing: -0.04em; }}
.ds-title-lg {{ margin: 0; font-size: 24px; letter-spacing: -0.02em; }}
.ds-title-md {{ margin: 0; font-size: 18px; }}
.ds-text {{ margin: 0; color: var(--ds-ink-soft); line-height: 1.65; }}
.ds-card.hero .ds-text {{ color: rgba(255,255,255,.84); }}
.ds-muted {{ color: var(--ds-muted); }}

.ds-pill {{
  display: inline-flex;
  align-items: center;
  padding: 10px 14px;
  border-radius: var(--ds-r-pill);
  font-size: 13px;
  font-weight: 700;
  border: 1px solid var(--ds-border);
  background: var(--ds-surface-alt);
}}
.ds-pill.good {{ color: var(--ds-good); }}
.ds-pill.watch {{ color: var(--ds-watch); }}
.ds-pill.risk {{ color: var(--ds-risk); }}

.ds-button-row {{ display: flex; gap: var(--ds-sp-sm); flex-wrap: wrap; }}
.ds-btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 13px;
  font-weight: 800;
  border: 1px solid transparent;
  cursor: pointer;
  transition: transform .15s ease, box-shadow .15s ease;
}}
.ds-btn:hover {{ transform: translateY(-1px); }}
.ds-btn.primary {{ background: var(--ds-brand); color: #fff; box-shadow: 0 10px 20px rgba(194,65,12,.22); }}
.ds-btn.secondary {{ background: var(--ds-brand-alt); color: #fff; box-shadow: 0 10px 20px rgba(15,118,110,.22); }}
.ds-btn.ghost {{ background: var(--ds-surface); color: var(--ds-ink); border-color: var(--ds-border); }}

.ds-input,
.ds-select,
.ds-textarea {{
  width: 100%;
  border-radius: 12px;
  border: 1px solid var(--ds-border);
  background: var(--ds-surface);
  color: var(--ds-ink);
  padding: 10px 12px;
  font: inherit;
}}
.ds-input:focus,
.ds-select:focus,
.ds-textarea:focus {{ outline: 2px solid rgba(29,78,216,.24); outline-offset: 1px; }}
.ds-label {{ display: block; font-size: 12px; color: var(--ds-muted); margin-bottom: 6px; text-transform: uppercase; letter-spacing: .06em; }}

.ds-kpi {{
  border: 1px solid var(--ds-border);
  background: var(--ds-surface);
  border-radius: var(--ds-r-md);
  padding: var(--ds-sp-lg);
}}
.ds-kpi-label {{ font-size: 12px; color: var(--ds-muted); text-transform: uppercase; letter-spacing: .08em; }}
.ds-kpi-value {{ margin-top: 8px; font-size: 30px; line-height: 1; font-weight: 800; letter-spacing: -.04em; }}
.ds-kpi-hint {{ margin-top: 8px; color: var(--ds-muted); font-size: 13px; line-height: 1.55; }}

.ds-tag {{
  display: inline-flex;
  align-items: center;
  border-radius: var(--ds-r-pill);
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .06em;
}}
.ds-tag.good {{ background: rgba(21,128,61,.10); color: var(--ds-good); }}
.ds-tag.watch {{ background: rgba(180,83,9,.10); color: var(--ds-watch); }}
.ds-tag.risk {{ background: rgba(185,28,28,.10); color: var(--ds-risk); }}

@media (max-width: 980px) {{
  .ds-grid.cols-2,
  .ds-grid.cols-3,
  .ds-grid.cols-4 {{ grid-template-columns: 1fr; }}
  .ds-shell {{ padding: var(--ds-sp-lg) var(--ds-sp-md); }}
}}
"""


def write_design_system_css(path="design_system.css"):
    output = Path(path)
    output.write_text(build_design_system_css(), encoding="utf-8")
    return str(output)


if __name__ == "__main__":
    print(write_design_system_css())
