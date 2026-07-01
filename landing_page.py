import html
from pathlib import Path

from setup_wizard import build_setup_summary


def _status_label():
    surfaces = [Path("client_dashboard.html"), Path("client_setup_wizard.html"), Path("executive_briefing.html")]
    generated = sum(1 for surface in surfaces if surface.exists())
    if generated >= 3:
        return "Launch-ready"
    if generated >= 2:
        return "Pilot-ready"
    return "First draft"


def _fcard(icon, title, desc):
    return (
        f'<div class="bg-white/80 backdrop-blur border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">'
        f'<div class="text-3xl mb-3">{icon}</div>'
        f'<h3 class="font-bold text-slate-900 mb-2">{html.escape(title)}</h3>'
        f'<p class="text-slate-500 text-sm leading-relaxed">{html.escape(desc)}</p>'
        f'</div>'
    )


def build_landing_page_html():
    setup_summary = build_setup_summary()
    ready_count = setup_summary.get("ready_count", 0)
    total_sources = setup_summary.get("total_sources", 0)
    status_label = _status_label()

    m365_state = "Needs setup"
    for source in setup_summary.get("sources", []):
        if source.get("title") == "Microsoft 365":
            m365_state = source.get("label", "Needs setup")
            break


    feature_cards = "".join([
        _fcard("⚡", "Daily AI Briefing", "Executive-grade intelligence every morning, tailored to your business data."),
        _fcard("📊", "Trend Detection", "14-day historical comparison with anomaly detection — spot problems before they hit."),
        _fcard("🔗", "Google + Microsoft", "Connects Gmail, Google Calendar, Outlook, Teams, OneDrive, and Slack."),
        _fcard("📄", "Document Intelligence", "Reads PDFs and emails to extract decisions and action items automatically."),
        _fcard("📈", "Weekly Digest", "Visual trend table from local snapshots. No analytics database needed."),
        _fcard("🧭", "Setup Wizard", "Self-serve onboarding. Customers connect sources without developer help."),
    ])

    integrations = ["Gmail", "Google Calendar", "Outlook", "Microsoft Teams", "OneDrive", "Slack", "Notion", "PDFs"]
    integration_pills = "".join(
        f'<span class="px-4 py-2 bg-white/10 border border-white/20 rounded-full text-sm font-semibold text-white/80">{html.escape(i)}</span>'
        for i in integrations
    )

    return f"""<!doctype html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lucent — Executive Intelligence Platform</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>body{{font-family:'Inter',sans-serif;}}</style>
</head>
<body class="bg-gradient-to-br from-stone-50 via-sky-50 to-slate-50 antialiased text-slate-900">

  <nav class="sticky top-0 z-50 backdrop-blur-xl bg-white/80 border-b border-slate-200">
    <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-orange-600 to-red-700 flex items-center justify-center shadow">
          <span class="text-white font-black text-sm">L</span>
        </div>
        <span class="font-black text-xl tracking-tight">Lucent</span>
      </div>
      <div class="hidden md:flex gap-8 text-sm font-semibold text-slate-500">
        <a href="#features" class="hover:text-orange-600 transition-colors">Features</a>
        <a href="#integrations" class="hover:text-orange-600 transition-colors">Integrations</a>
        <a href="#pricing" class="hover:text-orange-600 transition-colors">Pricing</a>
      </div>
      <div class="flex items-center gap-3">
        <a href="client_setup_wizard.html" class="text-sm font-semibold text-slate-500 hover:text-slate-900 transition-colors hidden sm:block">Setup</a>
        <a href="client_dashboard.html" class="px-4 py-2 bg-slate-900 text-white text-sm font-bold rounded-xl hover:bg-slate-700 transition-colors shadow-sm">Dashboard →</a>
      </div>
    </div>
  </nav>

  <section class="relative overflow-hidden bg-slate-950 py-28 text-center">
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_rgba(234,88,12,0.25),transparent_60%)]"></div>
    <div class="relative max-w-5xl mx-auto px-6">
      <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 border border-white/15 text-white/70 text-xs font-bold uppercase tracking-widest mb-8">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        {html.escape(status_label)} &nbsp;·&nbsp; {ready_count}/{total_sources} sources ready
      </div>
      <h1 class="text-5xl md:text-7xl font-black text-white leading-[0.92] tracking-[-0.04em] mb-6">
        Your business,<br><span class="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-amber-300">briefed by AI.</span>
      </h1>
      <p class="text-lg text-white/60 max-w-2xl mx-auto mb-10 leading-relaxed">
        Lucent turns your live data into a polished executive briefing every morning. Trend detection, market signals, team context — delivered where you work.
      </p>
      <div class="flex flex-wrap justify-center gap-4">
        <a href="client_dashboard.html" class="px-8 py-4 bg-white text-slate-900 font-extrabold rounded-2xl shadow-xl hover:bg-amber-50 hover:-translate-y-0.5 transition-all text-sm">Open dashboard →</a>
        <a href="client_setup_wizard.html" class="px-8 py-4 bg-white/10 text-white font-bold rounded-2xl border border-white/20 hover:bg-white/20 transition-all text-sm">Setup wizard</a>
      </div>
    </div>
  </section>

  <div class="bg-white border-y border-slate-200">
    <div class="max-w-6xl mx-auto px-6 py-4 flex flex-wrap justify-center gap-x-10 gap-y-2 text-sm font-semibold text-slate-400">
      <span>✓ Google Workspace</span><span>✓ Microsoft 365</span><span>✓ Slack</span><span>✓ Notion</span><span>✓ Free to start</span>
    </div>
  </div>

  <section id="features" class="max-w-6xl mx-auto px-6 py-24">
    <div class="text-center mb-16">
      <p class="text-orange-600 font-bold text-xs uppercase tracking-widest mb-3">What Lucent does</p>
      <h2 class="text-4xl md:text-5xl font-black tracking-tight mb-4">Intelligence that fits<br>your workflow.</h2>
      <p class="text-slate-500 max-w-lg mx-auto">Six capabilities that turn raw business data into decisive daily intelligence.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      {feature_cards}
    </div>
  </section>

  <section id="integrations" class="bg-slate-950 py-24">
    <div class="max-w-6xl mx-auto px-6 text-center">
      <p class="text-amber-400 font-bold text-xs uppercase tracking-widest mb-3">Integrations</p>
      <h2 class="text-4xl font-black text-white tracking-tight mb-4">Connects to every tool<br>your team already uses.</h2>
      <p class="text-slate-400 max-w-lg mx-auto mb-12 text-sm">One-click OAuth. No code. No IT ticket. Your data stays yours.</p>
      <div class="flex flex-wrap justify-center gap-3">{integration_pills}</div>
    </div>
  </section>

  <section class="max-w-6xl mx-auto px-6 py-24">
    <div class="text-center mb-16">
      <p class="text-orange-600 font-bold text-xs uppercase tracking-widest mb-3">How it works</p>
      <h2 class="text-4xl font-black tracking-tight">Up and running in three steps.</h2>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-10 text-center">
      <div>
        <div class="w-14 h-14 rounded-2xl bg-orange-600 text-white text-2xl font-black flex items-center justify-center mx-auto mb-5 shadow-lg">1</div>
        <h3 class="font-bold text-lg mb-2">Connect your sources</h3>
        <p class="text-slate-500 text-sm leading-relaxed">Use the setup wizard to connect Gmail, Microsoft 365, Slack, or Notion with one OAuth click each.</p>
      </div>
      <div>
        <div class="w-14 h-14 rounded-2xl bg-teal-700 text-white text-2xl font-black flex items-center justify-center mx-auto mb-5 shadow-lg">2</div>
        <h3 class="font-bold text-lg mb-2">Lucent reads and analyses</h3>
        <p class="text-slate-500 text-sm leading-relaxed">Every morning, Lucent pulls live data, detects trends, and runs AI analysis across tasks, CRM, inventory, emails, and market signals.</p>
      </div>
      <div>
        <div class="w-14 h-14 rounded-2xl bg-slate-800 text-white text-2xl font-black flex items-center justify-center mx-auto mb-5 shadow-lg">3</div>
        <h3 class="font-bold text-lg mb-2">Read your briefing</h3>
        <p class="text-slate-500 text-sm leading-relaxed">Receive a polished executive briefing in your inbox, Notion, and dashboard. Scored. Prioritised. Actionable.</p>
      </div>
    </div>
  </section>

  <section class="max-w-6xl mx-auto px-6 pb-24">
    <div class="bg-white border border-slate-200 rounded-3xl p-8 md:p-10 shadow-sm">
      <p class="text-orange-600 font-bold text-xs uppercase tracking-widest mb-3">Setup first</p>
      <h2 class="text-3xl font-black tracking-tight mb-4">Microsoft 365 onboarding checklist</h2>
      <p class="text-slate-500 text-sm mb-6">Current status: <strong>{html.escape(m365_state)}</strong>. Lucent uses the free Microsoft Graph API and needs a tenant app registration before data can be read.</p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="font-bold text-slate-900 mb-3">Admin setup</h3>
          <ol class="text-sm text-slate-600 space-y-2 list-decimal list-inside">
            <li>Register an Azure app in Microsoft Entra ID.</li>
            <li>Grant Graph permissions: Mail.Read, Calendars.Read, Files.Read, ChannelMessage.Read.All.</li>
            <li>Complete admin consent for the tenant.</li>
          </ol>
        </div>
        <div>
          <h3 class="font-bold text-slate-900 mb-3">Lucent connection</h3>
          <ol class="text-sm text-slate-600 space-y-2 list-decimal list-inside">
            <li>Set <code>M365_ACCESS_TOKEN</code> in the environment.</li>
            <li>Create <code>m365_config.json</code> with Teams channel IDs (optional).</li>
            <li>Run briefing generation and confirm data appears in the dashboard.</li>
          </ol>
        </div>
      </div>
    </div>
  </section>

  <section id="pricing" class="bg-gradient-to-br from-stone-50 to-amber-50 py-24">
    <div class="max-w-6xl mx-auto px-6 text-center">
      <p class="text-orange-600 font-bold text-xs uppercase tracking-widest mb-3">Pricing</p>
      <h2 class="text-4xl font-black tracking-tight mb-4">Start free. Scale when ready.</h2>
      <p class="text-slate-500 max-w-md mx-auto mb-14 text-sm">No credit card required. No paid services needed for the pilot phase.</p>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto text-left">
        <div class="bg-white rounded-3xl border border-slate-200 p-8 shadow-sm">
          <p class="font-bold text-xs text-slate-400 uppercase tracking-wide mb-2">Starter</p>
          <p class="text-4xl font-black mb-1">Free</p>
          <p class="text-slate-400 text-sm mb-6">Forever. No card needed.</p>
          <ul class="space-y-2.5 text-sm text-slate-600 mb-8">
            <li class="flex gap-2"><span class="text-emerald-500">✓</span> 1 workspace</li>
            <li class="flex gap-2"><span class="text-emerald-500">✓</span> Daily briefing</li>
            <li class="flex gap-2"><span class="text-emerald-500">✓</span> 2 integrations</li>
            <li class="flex gap-2"><span class="text-emerald-500">✓</span> Weekly digest</li>
          </ul>
          <a href="client_setup_wizard.html" class="block text-center py-3 border border-slate-300 rounded-xl font-bold text-sm hover:bg-slate-50 transition-colors">Get started</a>
        </div>
        <div class="bg-slate-950 rounded-3xl border border-slate-800 p-8 shadow-2xl relative overflow-hidden">
          <div class="absolute top-4 right-4 px-3 py-1 bg-amber-400 text-slate-900 text-xs font-black rounded-full">Popular</div>
          <p class="font-bold text-xs text-slate-400 uppercase tracking-wide mb-2">Professional</p>
          <p class="text-4xl font-black text-white mb-1">$49<span class="text-xl font-medium text-slate-400">/mo</span></p>
          <p class="text-slate-400 text-sm mb-6">Per workspace.</p>
          <ul class="space-y-2.5 text-sm text-slate-300 mb-8">
            <li class="flex gap-2"><span class="text-amber-400">✓</span> Unlimited briefings</li>
            <li class="flex gap-2"><span class="text-amber-400">✓</span> All integrations</li>
            <li class="flex gap-2"><span class="text-amber-400">✓</span> Trend detection</li>
            <li class="flex gap-2"><span class="text-amber-400">✓</span> Priority support</li>
          </ul>
          <a href="client_setup_wizard.html" class="block text-center py-3 bg-white text-slate-900 rounded-xl font-extrabold text-sm hover:bg-amber-50 transition-colors">Start free trial</a>
        </div>
        <div class="bg-white rounded-3xl border border-slate-200 p-8 shadow-sm">
          <p class="font-bold text-xs text-slate-400 uppercase tracking-wide mb-2">Enterprise</p>
          <p class="text-4xl font-black mb-1">Custom</p>
          <p class="text-slate-400 text-sm mb-6">Volume + SLA.</p>
          <ul class="space-y-2.5 text-sm text-slate-600 mb-8">
            <li class="flex gap-2"><span class="text-emerald-500">✓</span> Multi-tenant</li>
            <li class="flex gap-2"><span class="text-emerald-500">✓</span> Custom connectors</li>
            <li class="flex gap-2"><span class="text-emerald-500">✓</span> Dedicated support</li>
            <li class="flex gap-2"><span class="text-emerald-500">✓</span> On-premise option</li>
          </ul>
          <a href="mailto:hello@lucent.ai" class="block text-center py-3 border border-slate-300 rounded-xl font-bold text-sm hover:bg-slate-50 transition-colors">Contact sales</a>
        </div>
      </div>
    </div>
  </section>

  <footer class="bg-slate-950 py-14">
    <div class="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-orange-600 to-red-700 flex items-center justify-center">
          <span class="text-white font-black text-sm">L</span>
        </div>
        <span class="font-black text-lg text-white tracking-tight">Lucent</span>
      </div>
      <div class="flex flex-wrap justify-center gap-6 text-sm text-slate-500">
        <a href="client_dashboard.html" class="hover:text-white transition-colors">Dashboard</a>
        <a href="client_setup_wizard.html" class="hover:text-white transition-colors">Setup wizard</a>
        <a href="executive_briefing.html" class="hover:text-white transition-colors">Briefing</a>
        <a href="design_system_preview.html" class="hover:text-white transition-colors">Design system</a>
      </div>
      <p class="text-slate-600 text-sm">© 2026 Lucent.</p>
    </div>
  </footer>

</body>
</html>
"""


def write_landing_page(path="landing_page.html"):
    output = Path(path)
    output.write_text(build_landing_page_html(), encoding="utf-8")
    return str(output)


if __name__ == "__main__":
    print(write_landing_page())
