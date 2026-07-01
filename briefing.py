# ============================================================
# OFFICE BRIEFING TOOL — Session 5 (Audited & Fixed)
# Reads data → AI briefing → delivers to:
# Notion · Gmail · Outlook · Google Calendar
# Fixes applied:
#   1. Notion text splitter bug fixed (1800 not 2000)
#   2. Completion % now shows as 45% not 0.45
#   3. Runs once per day only — duplicate run protection
#   4. Unused imports removed (googleapiclient, timedelta)
#   5. Unused variables removed (start_dt, end_dt)
#   6. Calendar event uses actual run time not hardcoded 7am
#   7. Single SMTP connection sends all emails efficiently
#   8. CRM score uses loss rate not raw count
#   9. Full run log written to briefing_log.txt
# ============================================================

import pandas as pd
from groq import Groq
from dotenv import load_dotenv
from notion_client import Client as NotionClient
from notion_client.errors import APIResponseError
from gmail_connector import fetch_recent_emails, format_emails_for_ai
from pdf_connector import process_all_pdfs, format_pdfs_for_ai
from news_connector import load_news_and_market, format_news_for_ai, format_market_for_ai, summarize_market_pulse, get_news_context_summary, capture_news_feedback, record_quick_feedback
from premium_report import write_premium_report
from status_sync import update_project_status
from trend_detection import build_trend_context
from slack_connector import build_slack_context
from m365_connector import build_m365_context
from dashboard import write_dashboard
from quick_response import create_approval_drafts, send_approved_drafts, summarize_queue, load_draft_queue
from action_register import build_action_register, write_action_register
from follow_up import build_follow_up_plan, write_follow_up_plan
from meeting_pipeline import build_meeting_execution_plan, write_meeting_execution_plan
from customer_health import build_customer_health_report, write_customer_health_report
from pipeline_risk import build_pipeline_risk_report, write_pipeline_risk_report
from approval_workflow import build_approval_workflow_report, write_approval_workflow_report
from kpi_digest import build_kpi_digest, write_kpi_digest
from communication_timeline import build_communication_timeline, write_communication_timeline
from recommendations import build_recommendations, write_recommendations
from sentiment import build_sentiment_report
from slack_approval import build_slack_approval_summary
from help_center import write_help_center
from revenue_forecast import build_revenue_forecast, write_revenue_forecast
from deal_progression import build_deal_progression, write_deal_progression
from renewal_reminders import build_renewal_reminders, write_renewal_reminders
import os
import sys
import smtplib
import json
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, datetime

# ── Logging setup ────────────────────────────────────────────
# All output goes to terminal AND to a log file simultaneously

LOG_FILE = "briefing_log.txt"

def safe_print(message):
    """Print a message safely even when the terminal encoding cannot handle emoji."""
    try:
        print(message)
    except UnicodeEncodeError:
        safe = message.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8", errors="ignore")
        print(safe)


def log(message):
    """Print to terminal and append to log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    safe_print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ── Run-once protection ──────────────────────────────────────
# Prevents duplicate briefings if computer is unlocked multiple times

RAN_TODAY_FILE = f"ran_today_{date.today().isoformat()}.lock"

if os.path.exists(RAN_TODAY_FILE):
    safe_print(f"✅ Briefing already sent today ({date.today()}). Skipping.")
    sys.exit()

# ── Load all keys from .env ──────────────────────────────────

load_dotenv()

groq_client    = Groq(api_key=os.getenv("GROQ_API_KEY"))
notion         = NotionClient(auth=os.getenv("NOTION_TOKEN"))
notion_page    = os.getenv("NOTION_PAGE_ID")
gmail_address  = os.getenv("GMAIL_ADDRESS")
gmail_password = os.getenv("GMAIL_APP_PASSWORD")
outlook_addr   = os.getenv("OUTLOOK_ADDRESS")
gcal_id        = os.getenv("GCAL_ID")

# AI provider selection: 'groq' (default) or 'roo'
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq").lower()
ROO_API_KEY = os.getenv("ROO_API_KEY")


def get_ai_response(prompt, model="llama-3.3-70b-versatile"):
    """Return a text response for `prompt` using the configured AI provider.

    Supports 'groq' (existing) and 'roo' (if installed and configured).
    Raises RuntimeError with actionable message when provider is unavailable.
    """
    provider = AI_PROVIDER

    if provider == "groq":
        try:
            resp = groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Groq API error: {e}") from e

    if provider == "roo":
        try:
            import roo
        except Exception as e:
            raise RuntimeError("Roo SDK not installed in the virtualenv. Install your provider's SDK (e.g. pip install roo) and set ROO_API_KEY in .env") from e

        # Try common Roo client patterns (best-effort):
        try:
            # Pattern 1: roo.Client(api_key=...)
            if hasattr(roo, "Client"):
                client = roo.Client(api_key=ROO_API_KEY)
                if hasattr(client, "chat") and hasattr(client.chat, "create"):
                    resp = client.chat.create(message=prompt)
                    return getattr(resp, 'content', getattr(resp, 'text', str(resp)))
                if hasattr(client, "completions") and hasattr(client.completions, "create"):
                    resp = client.completions.create(prompt=prompt)
                    return getattr(resp, 'text', str(resp))

            # Pattern 2: top-level roo.chat.completions.create
            if hasattr(roo, "chat") and hasattr(roo.chat, "completions"):
                resp = roo.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
                # attempt to extract text
                try:
                    return resp.choices[0].message.content
                except Exception:
                    return str(resp)

        except Exception as e:
            raise RuntimeError(f"Roo client error: {e}") from e

        raise RuntimeError("Roo is installed but no compatible client method was found. Provide a small SDK usage snippet and I can adapt this helper.")


# ── Load data ────────────────────────────────────────────────

try:
    tasks     = pd.read_csv("tasks.csv")
    inventory = pd.read_csv("inventory.csv")
    crm       = pd.read_csv("crm.csv")
except FileNotFoundError as e:
    log(f"❌ Could not find data file: {e}")
    sys.exit()

loaded_at  = datetime.now().strftime("%I:%M %p")
run_hour   = datetime.now().hour
run_minute = datetime.now().minute
today      = date.today().strftime("%A, %d %B %Y")

log(f"✅ Data loaded at {loaded_at}")

# ── Analyse tasks ────────────────────────────────────────────

total_tasks   = len(tasks)
completed     = tasks[tasks["Status"] == "Completed"]
in_progress   = tasks[tasks["Status"] == "In Progress"]
pending       = tasks[tasks["Status"] == "Pending"]
high_priority = tasks[
    (tasks["Priority"] == "High") &
    (tasks["Status"] != "Completed")
]
overdue = tasks[
    (tasks["Status"] != "Completed") &
    (pd.to_datetime(tasks["Due_Date"], errors="coerce") < pd.Timestamp(date.today()))
]

task_score = max(100 - len(high_priority)*20 - len(overdue)*15 - len(pending)*5, 0)

# Fix 2: Convert completion decimals to percentages for AI
def fmt_pct(val):
    try:
        return f"{int(float(val) * 100)}%"
    except:
        return str(val)

high_priority_display = high_priority.copy()
high_priority_display["Completion_%"] = high_priority_display["Completion_%"].apply(fmt_pct)

in_progress_display = in_progress.copy()
in_progress_display["Completion_%"] = in_progress_display["Completion_%"].apply(fmt_pct)

tasks_summary = f"""
TASKS ({total_tasks} total):
- Completed: {len(completed)}
- In Progress: {len(in_progress)}
- Pending: {len(pending)}
- Overdue: {len(overdue)}
High priority not completed:
{high_priority_display[['Task_Name','Status','Assignee','Due_Date','Completion_%']].to_string(index=False) if len(high_priority) > 0 else 'None'}
In progress:
{in_progress_display[['Task_Name','Assignee','Completion_%','Due_Date']].to_string(index=False) if len(in_progress) > 0 else 'None'}
"""

# ── Analyse inventory ────────────────────────────────────────

below_reorder = inventory[inventory["Stock_Level"] < inventory["Reorder_Point"]]
critical      = inventory[inventory["Stock_Level"] < inventory["Reorder_Point"] * 0.5]
discontinued  = inventory[inventory["Discontinued"] == True]
healthy       = inventory[
    (inventory["Stock_Level"] >= inventory["Reorder_Point"]) &
    (inventory["Discontinued"] == False)
]

inv_score = max(100 - len(below_reorder)*25 - len(critical)*20 - len(discontinued)*10, 0)

inventory_summary = f"""
INVENTORY ({len(inventory)} products):
- Healthy: {len(healthy)} | Below reorder: {len(below_reorder)} | Critical: {len(critical)} | Discontinued active: {len(discontinued)}
Needs reorder:
{below_reorder[['Product_Name','Stock_Level','Reorder_Point','Supplier']].to_string(index=False) if len(below_reorder) > 0 else 'None'}
Discontinued still active:
{discontinued[['SKU','Product_Name']].to_string(index=False) if len(discontinued) > 0 else 'None'}
"""

# ── Analyse CRM ──────────────────────────────────────────────

qualified    = crm[crm["Status"] == "Qualified"]
contacted    = crm[crm["Status"] == "Contacted"]
lost         = crm[crm["Status"] == "Lost"]
active_value = crm[crm["Status"] != "Lost"]["Lead_Value"].sum()
total_leads  = len(crm)

# Fix 8: Use loss rate not raw count for fairer scoring
loss_rate  = (len(lost) / total_leads * 100) if total_leads > 0 else 0
crm_score  = max(100 - int(loss_rate * 1.5) - (20 if len(qualified) == 0 else 0), 0)

crm_summary = f"""
CRM ({total_leads} leads):
- Qualified: {len(qualified)} | Contacted: {len(contacted)} | Lost: {len(lost)}
- Loss rate: {loss_rate:.0f}%
- Active pipeline: ${active_value:,.0f}
Qualified leads:
{qualified[['Lead_Name','Company','Lead_Value','Last_Contact']].to_string(index=False) if len(qualified) > 0 else 'None'}
"""

roadmap_items = high_priority.head(2)[["Task_Name","Assignee"]].to_dict(orient="records")
roadmap_products = below_reorder.head(2)["Product_Name"].tolist()
roadmap_focus = ", ".join([f"{r['Task_Name']} ({r['Assignee']})" for r in roadmap_items]) if roadmap_items else 'None'
roadmap_summary = f"""
PROJECT ROADMAP — Execution snapshot and next milestones:
- High-priority tasks remaining: {len(high_priority)}.
- Immediate actions: {roadmap_focus}.
- Pipeline momentum: ${active_value:,.0f} active value; {len(qualified)} qualified lead(s).
- Inventory risk: {len(below_reorder)} below reorder, {len(critical)} critical.
"""

# ── Load inbox intelligence ────────────────────────────────────

emails, email_error = fetch_recent_emails(hours_back=24, max_emails=10)
quick_response_summary = "QUICK RESPONSE DRAFTS: disabled (set QUICK_REPLY_ENABLED=1 to enable)."
action_register_summary = "Unified action register: not generated yet."
quick_response_queue = {"drafts": []}
if email_error:
    log(f"⚠️ Gmail connector issue: {email_error}")
    email_summary = f"Gmail connector error: {email_error}"
else:
    log(f"✅ Email intelligence loaded: {len(emails)} emails")
    email_summary = format_emails_for_ai(emails)
    quick_reply_enabled = os.getenv("QUICK_REPLY_ENABLED", "").strip().lower() in {"1", "true", "yes", "on"}
    if quick_reply_enabled:
        max_drafts = int(os.getenv("QUICK_REPLY_MAX_DRAFTS", "3"))
        queue = create_approval_drafts(
            emails,
            ai_generate=lambda p: get_ai_response(p),
            max_drafts=max_drafts,
            queue_path="response_drafts.json",
            audit_path="response_audit_log.jsonl",
        )
        quick_response_summary = summarize_queue(queue)
        log(f"✅ Quick response drafts prepared: {len(queue.get('drafts', []))} (approval required)")

    quick_response_queue = load_draft_queue()

documents = process_all_pdfs()
log(f"✅ Document intelligence loaded: {len(documents)} file(s)")
documents_summary = format_pdfs_for_ai(documents)

news, market = load_news_and_market(max_articles=6)
log(f"✅ News intelligence loaded: {len(news)} articles")
log(f"✅ Market intelligence loaded: {len(market)} entries")
news_summary = format_news_for_ai(news)
market_summary = format_market_for_ai(market)
market_signal_summary = summarize_market_pulse(market)


def build_one_click_feedback_links(articles, max_links=3):
    base_url = os.getenv("NEWS_FEEDBACK_BASE_URL", "http://127.0.0.1:8001").rstrip("/")
    seen = set()
    links = []
    for article in articles:
        topic = str(article.get("topic", "")).strip()
        if not topic:
            continue
        key = topic.lower()
        if key in seen:
            continue
        seen.add(key)
        vote_url = f"{base_url}/vote?topic={urllib.parse.quote(topic)}"
        links.append((topic, vote_url))
        if len(links) >= max_links:
            break
    return links


one_click_feedback_links = build_one_click_feedback_links(news)

market_changes = [item.get("changePercent", 0.0) for item in market if item.get("changePercent") is not None]
if market_changes:
    avg_market_change = sum(market_changes) / len(market_changes)
    if avg_market_change > 0.25:
        market_sentiment = "positive"
    elif avg_market_change < -0.25:
        market_sentiment = "negative"
    else:
        market_sentiment = "mixed"
    market_signal_score = max(0, min(100, round(50 + avg_market_change * 10)))
else:
    avg_market_change = 0.0
    market_sentiment = "neutral"
    market_signal_score = 50
market_signal_label = (
    "Market strength" if market_signal_score > 60 else
    "Market weakness" if market_signal_score < 40 else
    "Market mixed"
)
# ── Overall score ────────────────────────────────────────────

overall_score = round((task_score + inv_score + crm_score) / 3)
day_rating    = "🟢 Good" if overall_score >= 80 else "🟡 Needs Attention" if overall_score >= 60 else "🔴 High Alert"

# ── Build prompt ─────────────────────────────────────────────

user_industry = os.getenv("USER_INDUSTRY", "").strip()
user_region = os.getenv("USER_REGION", "").strip()
user_interests = [interest.strip() for interest in os.getenv("USER_INTERESTS", "").split(",") if interest.strip()]
profile_context = ""
if user_industry or user_region or user_interests:
    profile_context = (
        f"User profile: industry={user_industry or 'general'}, region={user_region or 'global'}, interests={', '.join(user_interests) or 'general business'}."
    )
news_context = get_news_context_summary()
trend_context = build_trend_context()
slack_context = build_slack_context()
m365_context = build_m365_context()

action_register = build_action_register(
    tasks,
    emails=emails,
    slack_context=slack_context,
    quick_response_queue=quick_response_queue,
)
action_register_summary = action_register["summary"]
write_action_register(
    tasks_df=tasks,
    emails=emails,
    slack_context=slack_context,
    quick_response_queue=quick_response_queue,
)
log(f"✅ {action_register_summary}")

follow_up_plan = build_follow_up_plan(
    tasks,
    action_register=action_register,
    quick_response_queue=quick_response_queue,
)
follow_up_summary = follow_up_plan["summary"]
write_follow_up_plan(
    tasks_df=tasks,
    action_register=action_register,
    quick_response_queue=quick_response_queue,
)
log(f"✅ {follow_up_summary}")

meeting_execution_plan = build_meeting_execution_plan(
    action_register=action_register,
    follow_up_plan=follow_up_plan,
)
meeting_execution_summary = meeting_execution_plan["summary"]
write_meeting_execution_plan(
    action_register=action_register,
    follow_up_plan=follow_up_plan,
)
log(f"✅ {meeting_execution_summary}")

customer_health_report = build_customer_health_report(
    crm,
    action_register=action_register,
    follow_up_plan=follow_up_plan,
    meeting_execution_plan=meeting_execution_plan,
)
customer_health_summary = customer_health_report["summary"]
write_customer_health_report(
    crm_df=crm,
    action_register=action_register,
    follow_up_plan=follow_up_plan,
    meeting_execution_plan=meeting_execution_plan,
)
log(f"✅ {customer_health_summary}")

pipeline_risk_report = build_pipeline_risk_report(
    crm,
    action_register=action_register,
    follow_up_plan=follow_up_plan,
    meeting_execution_plan=meeting_execution_plan,
)
pipeline_risk_summary = pipeline_risk_report["summary"]
write_pipeline_risk_report(
    crm_df=crm,
    action_register=action_register,
    follow_up_plan=follow_up_plan,
    meeting_execution_plan=meeting_execution_plan,
)
log(f"✅ {pipeline_risk_summary}")

approval_workflow_report = build_approval_workflow_report()
approval_workflow_summary = approval_workflow_report["summary"]
write_approval_workflow_report()
log(f"✅ {approval_workflow_summary}")

kpi_report = build_kpi_digest()
kpi_summary = kpi_report["summary"]
write_kpi_digest()
log(f"✅ {kpi_summary}")

communication_timeline = build_communication_timeline(
    crm,
    emails=emails,
    tasks_df=tasks,
)
comm_timeline_summary = communication_timeline["summary"]
write_communication_timeline(crm_df=crm, emails=emails, tasks_df=tasks)
log(f"✅ {comm_timeline_summary}")

recommendations_report = build_recommendations(
    action_register=action_register,
    follow_up_plan=follow_up_plan,
    customer_health_report=customer_health_report,
    pipeline_risk_report=pipeline_risk_report,
    kpi_digest=kpi_report,
    approval_workflow_report=approval_workflow_report,
)
recommendations_summary = recommendations_report["summary"]
write_recommendations(
    action_register=action_register,
    follow_up_plan=follow_up_plan,
    customer_health_report=customer_health_report,
    pipeline_risk_report=pipeline_risk_report,
    kpi_digest=kpi_report,
    approval_workflow_report=approval_workflow_report,
)
log(f"✅ {recommendations_summary}")

sentiment_report = build_sentiment_report(emails)
sentiment_summary = sentiment_report["summary"]
log(f"✅ {sentiment_summary}")

slack_approval_status = build_slack_approval_summary()
slack_approval_summary = slack_approval_status["summary"]
log(f"✅ {slack_approval_summary}")

write_help_center()
log("✅ Help center generated")

revenue_forecast_report = build_revenue_forecast(crm)
revenue_forecast_summary = revenue_forecast_report["summary"]
write_revenue_forecast(crm_df=crm)
log(f"✅ {revenue_forecast_summary}")

deal_progression_report = build_deal_progression(crm)
deal_progression_summary = deal_progression_report["summary"]
write_deal_progression(crm_df=crm)
log(f"✅ {deal_progression_summary}")

renewal_reminders_report = build_renewal_reminders(crm)
renewal_reminders_summary = renewal_reminders_report["summary"]
write_renewal_reminders(crm_df=crm)
log(f"✅ {renewal_reminders_summary}")

prompt = f"""
You are a polished executive assistant briefing a senior business leader at the start of their day.
Your tone is direct, confident, and concise — no fluff, no buzzwords, just clear business impact.
The reader is an enterprise leader who needs a premium daily summary they can act on immediately.

Today is {today}. Data refreshed at {loaded_at}.
Overall Day Score: {overall_score}/100 — {day_rating}
Strategic Pulse Score: {market_signal_score}/100 — {market_signal_label}
{profile_context}
{news_context}

{trend_context}

{slack_context}

{m365_context}

{tasks_summary}
{inventory_summary}
{crm_summary}

Write the morning briefing in this exact structure:

---
GOOD MORNING
[One warm natural opening sentence based on the overall score]

DAY SCORE: {overall_score}/100 — {day_rating}
Data refreshed: {loaded_at}

---
📋 TASKS  [{task_score}/100]
[2-3 sentences. Flag overdue items by name and assignee.
Note completion percentages — they are already formatted as e.g. 45%, use them as-is.]

🔧 USEFUL TOOLS FOR TASKS:
[2-3 specific tool suggestions based on the actual issues]

---
📦 INVENTORY  [{inv_score}/100]
[2-3 sentences. Name products needing action and their suppliers.]

🔧 USEFUL TOOLS FOR INVENTORY:
[2-3 specific tool suggestions]

---
💼 CRM  [{crm_score}/100]
[2-3 sentences. Name qualified leads and values. Mention loss rate if notable.]

🔧 USEFUL TOOLS FOR CRM:
[2-3 specific tool suggestions]

---
🧭 PROJECT ROADMAP
[Summarise the direction and next execution milestones based on pending tasks, pipeline momentum, and inventory risk. Keep it concise and action-oriented.]
{roadmap_summary}

---
📧 EMAILS
[Summarise the key email activity from the manager’s inbox over the last 24 hours. If no emails require attention, say that the inbox was clear.]
{email_summary}

---
✉️ QUICK RESPONSE DRAFTS
[Summarise draft-reply readiness, including what still needs approval before sending.]
{quick_response_summary}

---
📄 DOCUMENTS
[Summarise any new documents from the inbox folder and what they mean for today’s priorities. If there are no files, say the document inbox is empty.]
{documents_summary}

---
📈 NEWS
[Summarise the latest business headlines. Highlight strategic themes and any risk signals that should influence the day's priorities.]
{news_summary}

---
📈 MARKET PULSE
[Summarise the market movement and its implications for today's priorities. Flag whether the pulse is positive, negative, or mixed, and identify the most important signal.]
{market_signal_summary}

{market_summary}

---
📊 RISK & OPPORTUNITY
[Summarise the top risk and top opportunity from today's data, using business language suitable for a senior executive. Keep it short, sharp, and actionable.]

---
✅ TOP 3 PRIORITIES TODAY
1. [Most urgent — specific and named]
2. [Second priority — specific and named]
3. [Third priority — specific and named]

---
🗂️ ACTION REGISTER
[Summarise the most important cross-system tasks from tasks, email, Slack, and pending reply approvals. Keep it short and operational.]
{action_register_summary}

---
🔁 FOLLOW-UP AUTOPILOT
[Summarise the most important overdue items and nudge opportunities that should be chased next. Keep it short and operational.]
{follow_up_summary}

---
📅 MEETING TO EXECUTION
[Summarise how meeting notes and live work items convert into owners, deadlines, and next steps. Keep it short and operational.]
{meeting_execution_summary}

---
🛡️ CUSTOMER HEALTH RADAR
[Summarise the strongest customer opportunities and the accounts/leads most at risk, based on CRM and follow-up signals. Keep it short and operational.]
{customer_health_summary}

---
🚨 PIPELINE RISK RADAR
[Summarise the deals most likely to slip or need escalation, based on CRM recency, value, and open work signals. Keep it short and operational.]
{pipeline_risk_summary}

---
📋 APPROVAL WORKFLOW
[Summarise how many drafts are pending approval, which ones are most urgent, and the recommended order for review. Keep it short and actionable.]
{approval_workflow_summary}

---
📬 EMAIL SENTIMENT
[Flag the most urgent emails from today's inbox based on tone, keywords, and urgency signals. Keep it brief.]
{sentiment_summary}

---
💡 RECOMMENDATIONS
[Summarise the top 2 smart recommendations for today based on all live signals.]
{recommendations_summary}

---
📈 KPI DIGEST
[Note any KPIs that are trending in the wrong direction and what that means for today.]
{kpi_summary}

---
💰 REVENUE FORECAST
[Summarise projected revenue for the next 30, 60, and 90 days from the active pipeline. Keep it short and specific.]
{revenue_forecast_summary}

---
⏳ DEAL PROGRESSION
[Flag any deals stuck in their current stage longer than expected and recommend the next push.]
{deal_progression_summary}

---
🔔 RENEWAL REMINDERS
[Highlight any upcoming or overdue contract renewals that need proactive outreach.]
{renewal_reminders_summary}

---
[One closing sentence like a good PA would say]
---

Keep under 450 words. Make it feel written by a person, not generated.
"""

# ── Generate briefing ────────────────────────────────────────

log("🤖 Generating briefing...")

try:
    briefing = get_ai_response(prompt)
except Exception as e:
    log(f"❌ AI generation error: {e}")
    sys.exit()

if one_click_feedback_links:
    quick_feedback = ["", "---", "NEWS FEEDBACK (one-click)"]
    for idx, (topic, url) in enumerate(one_click_feedback_links, start=1):
        quick_feedback.append(f"{idx}. 👍 {topic}: {url}")
    briefing = briefing.rstrip() + "\n" + "\n".join(quick_feedback) + "\n"

try:
    report_path = write_premium_report(
        "executive_briefing.html",
        today=today,
        loaded_at=loaded_at,
        overall_score=overall_score,
        day_rating=day_rating,
        market_signal_score=market_signal_score,
        market_signal_label=market_signal_label,
        news_context=news_context,
        roadmap_summary=roadmap_summary,
        briefing=briefing,
        one_click_feedback_links=one_click_feedback_links,
    )
    log(f"✅ Premium HTML report created: {report_path}")
    dashboard_path = write_dashboard()
    log(f"✅ Customer dashboard refreshed: {dashboard_path}")
except Exception as exc:
    log(f"⚠️ Premium HTML report skipped: {exc}")

print("\n" + "=" * 60)
print(f"  OFFICE BRIEFING — {today}")
print(f"  Data refreshed at {loaded_at}")
print("=" * 60)
print()
safe_print(briefing)
safe_print("")
safe_print("=" * 60)
safe_print(f"  Overall Score: {overall_score}/100 — {day_rating}")
safe_print("=" * 60 + "\n")

try:
    feedback = capture_news_feedback()
    if feedback.get("topics"):
        log(f"🧠 News feedback captured for: {', '.join(feedback['topics'].keys())}")
except Exception as exc:
    log(f"⚠️ Feedback capture skipped: {exc}")

try:
    record_quick_feedback("thumbs_up", topics=[os.getenv("USER_INDUSTRY", "").strip(), os.getenv("USER_REGION", "").strip()], source="briefing")
except Exception as exc:
    log(f"⚠️ Quick feedback save skipped: {exc}")

# ── DELIVER TO NOTION ────────────────────────────────────────

log("📓 Sending to Notion...")

def make_text_block(content):
    """Create a Notion paragraph block — safely under 1800 chars"""
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {"type": "text", "text": {"content": content[:1800]}}
            ]
        }
    }

def split_briefing_blocks(text):
    """Split briefing into 1800-char chunks — fix: advance by 1800 not 2000"""
    chunks = []
    while len(text) > 0:
        chunks.append(make_text_block(text[:1800]))
        text = text[1800:]   # ← Bug 1 fixed: was text[2000:]
    return chunks

try:
    notion.pages.retrieve(page_id=notion_page)
    blocks = [
        make_text_block(
            f"Day Score: {overall_score}/100 — {day_rating}\n"
            f"Data refreshed: {loaded_at}"
        ),
        {"object": "block", "type": "divider", "divider": {}},
    ] + split_briefing_blocks(briefing)

    created = notion.pages.create(
        parent={"page_id": notion_page},
        properties={
            "title": {
                "title": [{"text": {"content": f"Briefing — {today}"}}]
            }
        },
        children=blocks
    )
    log("   ✅ Notion page created")
    page_id = created.get("id")
    if page_id:
        try:
            summary_text = (
                f"Strategic Pulse: {market_signal_score}/100 — {market_signal_label}\n"
                f"Top actions: {roadmap_focus}\n"
                f"Pipeline: ${active_value:,.0f} — {len(qualified)} qualified lead(s)."
            )
            notion.blocks.children.append(
                block_id=page_id,
                children=[make_text_block(summary_text)]
            )
            log("   ✅ Notion summary appended")
        except Exception:
            pass
except APIResponseError as e:
    log(f"   ❌ Notion access error: {e}")
except Exception as e:
    log(f"   ❌ Notion error: {e}")

# ── DELIVER VIA EMAIL (single SMTP connection) ───────────────
# Fix 7: One connection, three emails — much more efficient

log("📧 Sending emails...")

subject    = f"Office Briefing — {today} | Score: {overall_score}/100 {day_rating}"
email_body = (
    f"OFFICE BRIEFING — {today}\n"
    f"Data refreshed: {loaded_at}\n"
    f"Overall Score: {overall_score}/100 — {day_rating}\n\n"
    f"{briefing}"
)

# Fix 5 + 6: Use actual run time for calendar event
run_time_str  = f"{run_hour:02d}{run_minute:02d}00"
end_hour      = run_hour if run_minute < 30 else run_hour + 1
end_minute    = (run_minute + 30) % 60
end_time_str  = f"{end_hour:02d}{end_minute:02d}00"
today_compact = date.today().isoformat().replace("-", "")

ical = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Office Briefing Tool//EN
BEGIN:VEVENT
DTSTART:{today_compact}T{run_time_str}
DTEND:{today_compact}T{end_time_str}
SUMMARY:Morning Briefing — Score {overall_score}/100 {day_rating}
DESCRIPTION:{briefing[:500].replace(chr(10), '\\n')}
END:VEVENT
END:VCALENDAR"""

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(gmail_address, gmail_password)

    # Email 1 — Gmail
    msg = MIMEMultipart()
    msg["From"]    = gmail_address
    msg["To"]      = gmail_address
    msg["Subject"] = subject
    msg.attach(MIMEText(email_body, "plain"))
    server.send_message(msg)
    log(f"   ✅ Gmail email sent to {gmail_address}")

    # Email 2 — Outlook
    msg2 = MIMEMultipart()
    msg2["From"]    = gmail_address
    msg2["To"]      = outlook_addr
    msg2["Subject"] = subject
    msg2.attach(MIMEText(email_body, "plain"))
    server.send_message(msg2)
    log(f"   ✅ Outlook email sent to {outlook_addr}")

    # Email 3 — Calendar invite
    msg3 = MIMEMultipart("mixed")
    msg3["From"]    = gmail_address
    msg3["To"]      = gcal_id
    msg3["Subject"] = f"📅 Morning Briefing — {today} | {overall_score}/100 {day_rating}"
    msg3.attach(MIMEText(email_body, "plain"))
    cal_part = MIMEText(ical, "calendar", "utf-8")
    cal_part.add_header("Content-Disposition", "attachment", filename="briefing.ics")
    msg3.attach(cal_part)
    server.send_message(msg3)
    log("   ✅ Calendar invite sent")

    server.quit()

except Exception as e:
    log(f"   ❌ Email error: {e}")

quick_reply_send_enabled = os.getenv("QUICK_REPLY_SEND_APPROVED", "").strip().lower() in {"1", "true", "yes", "on"}
if quick_reply_send_enabled:
    try:
        send_result = send_approved_drafts(
            smtp_host="smtp.gmail.com",
            smtp_port=587,
            smtp_username=gmail_address,
            smtp_password=gmail_password,
            from_email=gmail_address,
            queue_path="response_drafts.json",
            audit_path="response_audit_log.jsonl",
        )
        log(f"✅ Quick response send pass complete: sent={send_result.get('sent', 0)}, failed={send_result.get('failed', 0)}")
    except Exception as exc:
        log(f"⚠️ Quick response send skipped: {exc}")

# ── DELIVER TO SLACK / TEAMS (optional via env webhooks) ─────
def post_json(url, payload):
    try:
        import urllib.request
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        log(f"   ❌ Webhook POST error: {e}")
        return None

def send_slack_and_teams(summary):
    slack_url = os.getenv("SLACK_WEBHOOK_URL")
    teams_url = os.getenv("TEAMS_WEBHOOK_URL")
    if not slack_url and not teams_url:
        log("   ℹ️ No Slack/Teams webhooks configured; skipping.")
        return

    def build_slack_payload():
        return {
            "text": summary,
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Office Briefing — {today}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Day Score*\n{overall_score}/100 — {day_rating}"},
                        {"type": "mrkdwn", "text": f"*Strategic Pulse*\n{market_signal_score}/100 — {market_signal_label}"}
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Top Actions*\n{roadmap_focus if 'roadmap_focus' in globals() else 'See full briefing.'}"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": f"Refreshed at {loaded_at}"}
                    ]
                }
            ]
        }

    def build_teams_payload():
        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0B5FFF",
            "summary": "Office Briefing Summary",
            "title": f"Office Briefing — {today}",
            "sections": [
                {
                    "activityTitle": "Daily Executive Snapshot",
                    "facts": [
                        {"name": "Day Score", "value": f"{overall_score}/100 — {day_rating}"},
                        {"name": "Strategic Pulse", "value": f"{market_signal_score}/100 — {market_signal_label}"},
                        {"name": "Data Refreshed", "value": loaded_at}
                    ],
                    "text": f"Top actions: {roadmap_focus if 'roadmap_focus' in globals() else 'See full briefing.'}"
                }
            ]
        }

    slack_payload = build_slack_payload()
    teams_payload = build_teams_payload()
    if slack_url:
        try:
            post_json(slack_url, slack_payload)
            log("   ✅ Slack webhook sent")
        except Exception as e:
            log(f"   ❌ Slack error: {e}")
            try:
                post_json(slack_url, {"text": summary})
                log("   ✅ Slack webhook fallback text sent")
            except Exception as fallback_error:
                log(f"   ❌ Slack fallback error: {fallback_error}")

    if teams_url:
        try:
            post_json(teams_url, teams_payload)
            log("   ✅ Teams webhook sent")
        except Exception as e:
            log(f"   ❌ Teams error: {e}")
            try:
                post_json(teams_url, {"text": summary})
                log("   ✅ Teams webhook fallback text sent")
            except Exception as fallback_error:
                log(f"   ❌ Teams fallback error: {fallback_error}")

# Build a short summary for webhooks
short_summary = (
    f"Office Briefing — {today} | Score: {overall_score}/100 — {day_rating}\n"
    f"Strategic Pulse: {market_signal_score}/100 — {market_signal_label}\n"
    f"Top actions: {roadmap_focus if 'roadmap_focus' in globals() else 'See briefing.'}"
)

send_slack_and_teams(short_summary)

# ── Mark as ran today ────────────────────────────────────────
# Fix 3: Create lock file so script won't run again today

with open(RAN_TODAY_FILE, "w") as f:
    f.write(f"Ran at {loaded_at} on {today}\n")

# ── Clean up old lock files (older than 3 days) ──────────────

for filename in os.listdir("."):
    if filename.startswith("ran_today_") and filename.endswith(".lock"):
        file_date_str = filename.replace("ran_today_", "").replace(".lock", "")
        try:
            file_date = date.fromisoformat(file_date_str)
            if (date.today() - file_date).days > 3:
                os.remove(filename)
        except:
            pass

# ── Done ─────────────────────────────────────────────────────

try:
    if update_project_status(source="briefing run"):
        log("✅ Project status timestamp updated")
except Exception as exc:
    log(f"⚠️ Project status timestamp skipped: {exc}")

log("=" * 60)
log("  ✅ All deliveries complete")
log(f"  📓 Notion  |  📧 Gmail  |  📧 Outlook  |  📅 Calendar")
log("=" * 60)