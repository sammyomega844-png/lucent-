Lucent Executive Intelligence — README

Overview

This project generates a daily executive briefing from CSV data and integrated sources, then delivers it to Notion, email, and local customer-facing surfaces.

Required environment variables

- GROQ_API_KEY: Groq API key for AI generation
- NOTION_TOKEN: Notion integration token
- NOTION_PAGE_ID: Notion page id where briefings are created
- GMAIL_ADDRESS: Gmail account used to send emails
- GMAIL_APP_PASSWORD: App password for SMTP
- OUTLOOK_ADDRESS: Outlook recipient address
- GCAL_ID: Google Calendar recipient/email

Optional / fallback / integrations

- ALPHA_VANTAGE_API_KEY: Alphavantage key (optional, fallback market data)
- MARKET_SYMBOLS: Comma-separated symbols to fetch (default: SPY,DIA,QQQ)
- NEWS_TOPICS: Semicolon-separated topics for Google News RSS (overrides profile-based topics)
- USER_INDUSTRY: e.g. real estate
- USER_REGION: e.g. Dubai
- USER_INTERESTS: comma-separated interests, e.g. property market,mortgage rates,construction
- SLACK_WEBHOOK_URL: Incoming webhook URL to post summary to Slack
- TEAMS_WEBHOOK_URL: Incoming webhook URL to post summary to Microsoft Teams
- SLACK_BOT_TOKEN: Slack bot token for Slack channel context
- M365_ACCESS_TOKEN: Microsoft Graph access token for enterprise context
- QUICK_REPLY_ENABLED: set to 1/true to generate approval-required email reply drafts
- QUICK_REPLY_MAX_DRAFTS: maximum drafts to generate per run (default: 3)
- QUICK_REPLY_SEND_APPROVED: set to 1/true to send only approved drafts via SMTP
- AI_PROVIDER: "groq" (default) or "roo"
- ROO_API_KEY: Roo API key if `AI_PROVIDER=roo`

Running locally (Windows)

1. Activate your virtualenv:

```powershell
.\.venv\Scripts\Activate.ps1
```

2. Run the briefing:

```powershell
.\.venv\Scripts\python.exe briefing.py
```

3. Run the update/checker:

```powershell
.\.venv\Scripts\python.exe update.py
```

4. Generate the weekly executive digest (local, free):

```powershell
.\.venv\Scripts\python.exe weekly_digest.py
```

This writes `weekly_digest.html` and `weekly_digest.json` to the project folder.

5. Generate client-facing product surfaces:

```powershell
.\.venv\Scripts\python.exe dashboard.py
.\.venv\Scripts\python.exe setup_wizard.py
.\.venv\Scripts\python.exe landing_page.py
```

This writes `client_dashboard.html`, `client_setup_wizard.html/.json`, and `landing_page.html`.

Free premium enhancements (no paid services required)

- Local executive HTML report:
	- Each briefing run now generates `executive_briefing.html` in the project folder.
	- Open it in a browser for a premium-style executive view of the same briefing output.
- One-click news feedback:
	- Start the local feedback app:

```powershell
.\.venv\Scripts\python.exe feedback_app.py
```

	- Briefing output includes `NEWS FEEDBACK (one-click)` links.
	- Clicking a link saves that topic preference for future briefings.

CI (free)

- GitHub Actions workflow is included at `.github/workflows/ci.yml`.
- It runs syntax checks and all unit tests on pushes and pull requests.

Testing webhooks

- Slack quick test (replace <URL> with your `SLACK_WEBHOOK_URL`):

```powershell
Invoke-RestMethod -Method Post -Uri '<URL>' -Body (ConvertTo-Json @{text = 'Test message from Office Briefing'}) -ContentType 'application/json'
```

- Teams quick test uses the same JSON shape.

Notes

- The project uses a free market feed chain (Stooq → Yahoo JSON → Yahoo HTML → Alphavantage) and falls back gracefully.
- The scripts write logs to `briefing_log.txt` and `update_log.txt`.
- To enable Slack/Teams notifications, set `SLACK_WEBHOOK_URL` and/or `TEAMS_WEBHOOK_URL` in your `.env`.
- Project status tracking is for internal use only and is not linked from customer-facing surfaces.
