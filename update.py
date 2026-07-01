# ============================================================
# OFFICE UPDATE TOOL — Audited & Fixed
# Runs throughout the day — only alerts if something changed
# Fixes applied:
#   1. New items now detected (new tasks, leads, products)
#   2. Snapshot files cleaned up after 3 days
#   3. End-of-day wrap added at 6pm
#   4. Full run log written to update_log.txt
# ============================================================

import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, datetime

# ── Logging setup ────────────────────────────────────────────

LOG_FILE = "update_log.txt"

def safe_print(message):
    """Print a message safely even when the terminal encoding cannot handle emoji."""
    try:
        print(message)
    except UnicodeEncodeError:
        safe = message.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8", errors="ignore")
        print(safe)


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    safe_print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ── Load keys ────────────────────────────────────────────────

load_dotenv()

groq_client    = Groq(api_key=os.getenv("GROQ_API_KEY"))
gmail_address  = os.getenv("GMAIL_ADDRESS")
gmail_password = os.getenv("GMAIL_APP_PASSWORD")
outlook_addr   = os.getenv("OUTLOOK_ADDRESS")

# AI provider selection: 'groq' (default) or 'roo'
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq").lower()
ROO_API_KEY = os.getenv("ROO_API_KEY")


def get_ai_response(prompt, model="llama-3.3-70b-versatile"):
    """Lightweight AI abstraction used by update.py wrap generation.

    Mirrors the helper in briefing.py. Raises informative RuntimeError on missing SDK.
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
            raise RuntimeError("Roo SDK not installed. Install it and set ROO_API_KEY in .env") from e

        try:
            if hasattr(roo, "Client"):
                client = roo.Client(api_key=ROO_API_KEY)
                if hasattr(client, "chat") and hasattr(client.chat, "create"):
                    resp = client.chat.create(message=prompt)
                    return getattr(resp, 'content', getattr(resp, 'text', str(resp)))

            if hasattr(roo, "chat") and hasattr(roo.chat, "completions"):
                resp = roo.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
                try:
                    return resp.choices[0].message.content
                except Exception:
                    return str(resp)
        except Exception as e:
            raise RuntimeError(f"Roo client error: {e}") from e

        raise RuntimeError("Roo is installed but no compatible client method was found.")


now        = datetime.now().strftime("%I:%M %p")
now_hour   = datetime.now().hour
today      = date.today().isoformat()
today_fmt  = date.today().strftime("%A, %d %B %Y")

SNAPSHOT_FILE = f"snapshot_{today}.json"

# ── Load current data ────────────────────────────────────────

try:
    tasks     = pd.read_csv("tasks.csv")
    inventory = pd.read_csv("inventory.csv")
    crm       = pd.read_csv("crm.csv")
except FileNotFoundError as e:
    log(f"❌ Could not find data file: {e}")
    sys.exit()

# ── Build current snapshot ───────────────────────────────────

def build_snapshot(tasks, inventory, crm):
    return {
        "tasks": {
            row["Task_ID"]: {
                "name":       row["Task_Name"],
                "status":     row["Status"],
                "completion": float(row["Completion_%"]),
                "assignee":   row["Assignee"],
                "priority":   row["Priority"]
            }
            for _, row in tasks.iterrows()
        },
        "inventory": {
            row["SKU"]: {
                "name":         row["Product_Name"],
                "stock":        int(row["Stock_Level"]),
                "reorder":      int(row["Reorder_Point"]),
                "discontinued": bool(row["Discontinued"]),
                "supplier":     row["Supplier"]
            }
            for _, row in inventory.iterrows()
        },
        "crm": {
            row["Lead_ID"]: {
                "name":    row["Lead_Name"],
                "company": row["Company"],
                "status":  row["Status"],
                "value":   float(row["Lead_Value"])
            }
            for _, row in crm.iterrows()
        }
    }

current = build_snapshot(tasks, inventory, crm)

# ── Load or create snapshot ──────────────────────────────────

if not os.path.exists(SNAPSHOT_FILE):
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(current, f)
    log(f"📸 First run today — snapshot created at {now}")
    log("   No previous data to compare against. Run again later to detect changes.")
    sys.exit()

with open(SNAPSHOT_FILE, "r") as f:
    previous = json.load(f)

# ── Detect changes ───────────────────────────────────────────

changes = []

# ── Task changes ─────────────────────────────────────────────

for task_id, curr in current["tasks"].items():

    # Fix 1a: Detect brand new tasks
    if task_id not in previous["tasks"]:
        changes.append({
            "type":    "new_task",
            "emoji":   "📋",
            "urgency": "medium",
            "message": f"New task added: '{curr['name']}' assigned to {curr['assignee']} — {curr['priority']} priority"
        })
        continue

    prev = previous["tasks"][task_id]

    # Status changed
    if curr["status"] != prev["status"]:
        changes.append({
            "type":    "task_status",
            "emoji":   "📋",
            "urgency": "medium",
            "message": f"Task '{curr['name']}' changed from '{prev['status']}' to '{curr['status']}' — assigned to {curr['assignee']}"
        })

    # Completion jumped 20%+
    if curr["completion"] - prev["completion"] >= 0.20:
        changes.append({
            "type":    "task_progress",
            "emoji":   "📋",
            "urgency": "low",
            "message": f"Task '{curr['name']}' progressed from {int(prev['completion']*100)}% to {int(curr['completion']*100)}%"
        })

# Detect removed tasks
for task_id, prev in previous["tasks"].items():
    if task_id not in current["tasks"]:
        changes.append({
            "type":    "task_removed",
            "emoji":   "📋",
            "urgency": "low",
            "message": f"Task '{prev['name']}' was removed from the system"
        })

# ── Inventory changes ─────────────────────────────────────────

for sku, curr in current["inventory"].items():

    # Fix 1b: Detect brand new products
    if sku not in previous["inventory"]:
        changes.append({
            "type":    "new_product",
            "emoji":   "📦",
            "urgency": "low",
            "message": f"New product added: '{curr['name']}' (SKU: {sku}) — stock: {curr['stock']}, reorder at {curr['reorder']}"
        })
        continue

    prev = previous["inventory"][sku]

    # Stock dropped below reorder point
    if curr["stock"] < curr["reorder"] and prev["stock"] >= curr["reorder"]:
        changes.append({
            "type":    "stock_alert",
            "emoji":   "📦",
            "urgency": "high",
            "message": f"STOCK ALERT: '{curr['name']}' dropped below reorder point — now {curr['stock']} (reorder at {curr['reorder']}). Contact {curr['supplier']} immediately."
        })

    # Stock critically low (below 25% of reorder point)
    if curr["stock"] < curr["reorder"] * 0.25 and prev["stock"] >= curr["reorder"] * 0.25:
        changes.append({
            "type":    "stock_critical",
            "emoji":   "🔴",
            "urgency": "urgent",
            "message": f"CRITICAL: '{curr['name']}' nearly out of stock — {curr['stock']} units left. Immediate action required."
        })

    # Newly discontinued
    if curr["discontinued"] and not prev["discontinued"]:
        changes.append({
            "type":    "discontinued",
            "emoji":   "📦",
            "urgency": "low",
            "message": f"'{curr['name']}' (SKU: {sku}) marked as discontinued."
        })

# ── CRM changes ───────────────────────────────────────────────

for lead_id, curr in current["crm"].items():

    # Fix 1c: Detect brand new leads
    if lead_id not in previous["crm"]:
        changes.append({
            "type":    "new_lead",
            "emoji":   "💼",
            "urgency": "medium",
            "message": f"New lead added: '{curr['name']}' from {curr['company']} — ${curr['value']:,.0f} — status: {curr['status']}"
        })
        continue

    prev = previous["crm"][lead_id]

    if curr["status"] != prev["status"]:
        urgency = "high" if curr["status"] == "Qualified" else "medium"
        changes.append({
            "type":    "lead_status",
            "emoji":   "💼",
            "urgency": urgency,
            "message": f"Lead '{curr['name']}' from {curr['company']} moved from '{prev['status']}' to '{curr['status']}' — ${curr['value']:,.0f}"
        })

# ── End-of-day wrap (Fix 3) ──────────────────────────────────
# Runs at 6pm instead of a standard change alert

IS_END_OF_DAY = now_hour >= 17  # 5pm or later triggers wrap

if IS_END_OF_DAY:
    log(f"🌙 End of day detected ({now}) — generating daily wrap-up...")

    # Build wrap-up summary from current data
    completed_tasks = [t for t in current["tasks"].values() if t["status"] == "Completed"]
    open_tasks      = [t for t in current["tasks"].values() if t["status"] != "Completed"]
    high_pri_open   = [t for t in open_tasks if t["priority"] == "High"]
    qualified_leads = [l for l in current["crm"].values() if l["status"] == "Qualified"]
    stock_issues    = [p for p in current["inventory"].values() if p["stock"] < p["reorder"] and not p["discontinued"]]

    wrap_prompt = f"""
You are a personal assistant sending an end-of-day wrap to your manager.
Warm, brief, direct — like a trusted colleague signing off for the day.
Time: {now} on {today_fmt}

Here is the current state of the business:

TASKS:
- Completed today in system: {len(completed_tasks)}
- Still open: {len(open_tasks)}
- High priority still open: {len(high_pri_open)}
{chr(10).join([f"  • {t['name']} ({t['assignee']}) — {int(t['completion']*100)}%" for t in high_pri_open]) if high_pri_open else '  None'}

PIPELINE:
- Qualified leads ready to close: {len(qualified_leads)}
{chr(10).join([f"  • {l['name']} from {l['company']} — ${l['value']:,.0f}" for l in qualified_leads]) if qualified_leads else '  None'}

INVENTORY ISSUES STILL OPEN:
{chr(10).join([f"  • {p['name']} — {p['stock']} units (reorder at {p['reorder']})" for p in stock_issues]) if stock_issues else '  None'}

Write a short end-of-day wrap (under 150 words) that:
1. Opens with a warm one-liner acknowledging the end of the day
2. Briefly notes what's been handled and what's still outstanding
3. Flags the top 2 things to prioritise first thing tomorrow
4. Closes with one encouraging sentence to sign off

Keep it human, warm, and brief. No bullet points overload — flowing sentences.
"""

    try:
        wrap_response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": wrap_prompt}]
        )
        wrap_text = wrap_response.choices[0].message.content

        log(f"\n🌙 END OF DAY WRAP — {today_fmt}")
        log("=" * 50)
        print(wrap_text)
        log("=" * 50 + "\n")

        # Send wrap via email
        wrap_subject = f"🌙 End of Day Wrap — {today_fmt}"

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(gmail_address, gmail_password)

            for to_addr, label in [(gmail_address, "Gmail"), (outlook_addr, "Outlook")]:
                msg            = MIMEMultipart()
                msg["From"]    = gmail_address
                msg["To"]      = to_addr
                msg["Subject"] = wrap_subject
                msg.attach(MIMEText(wrap_text, "plain"))
                server.send_message(msg)
                log(f"   ✅ Wrap sent to {label}")

            server.quit()
        except Exception as e:
            log(f"   ❌ Wrap email error: {e}")

    except Exception as e:
        log(f"❌ Wrap generation error: {e}")

    # Update snapshot and exit — no regular change alert at end of day
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(current, f)
    log(f"📸 Snapshot updated at {now}")
    sys.exit()

# ── No changes — stay silent ─────────────────────────────────

if not changes:
    log(f"✅ Check at {now} — no changes detected. Staying silent.")
    sys.exit()

# ── Changes found — generate alert ───────────────────────────

log(f"⚡ {len(changes)} change(s) detected at {now} — generating alert...")

urgency_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
changes.sort(key=lambda x: urgency_order.get(x["urgency"], 99))

changes_text = "\n".join([f"{c['emoji']} {c['message']}" for c in changes])

alert_prompt = f"""
You are a personal assistant sending a quick mid-day update to your manager.
Keep it short, warm and direct — a quick heads up, not a full briefing.
Time: {now}

These changes were detected since the morning briefing:
{changes_text}

Write a short update message (under 150 words) that:
1. Opens with one casual sentence acknowledging the time and that there are updates
2. Lists each change clearly with what action if any is needed
3. Closes with one short sentence

Do not repeat the full morning briefing. Just the updates. Keep it conversational.
"""

try:
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": alert_prompt}]
    )
    alert = response.choices[0].message.content
except Exception as e:
    log(f"❌ Groq error: {e}")
    sys.exit()

print(alert)

# ── Send alert emails ─────────────────────────────────────────

urgent_count  = len([c for c in changes if c["urgency"] in ["urgent", "high"]])
alert_subject = f"⚡ Update — {len(changes)} change(s) at {now}" + (" 🔴 URGENT" if urgent_count > 0 else "")

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(gmail_address, gmail_password)

    for to_addr, label in [(gmail_address, "Gmail"), (outlook_addr, "Outlook")]:
        msg            = MIMEMultipart()
        msg["From"]    = gmail_address
        msg["To"]      = to_addr
        msg["Subject"] = alert_subject
        msg.attach(MIMEText(alert, "plain"))
        server.send_message(msg)
        log(f"   ✅ Alert sent to {label}")

    server.quit()
except Exception as e:
    log(f"   ❌ Email error: {e}")

# ── Update snapshot ───────────────────────────────────────────

with open(SNAPSHOT_FILE, "w") as f:
    json.dump(current, f)

log(f"📸 Snapshot updated at {now}")
log(f"✅ Update complete — {len(changes)} change(s) reported")

# ── Clean up old snapshot files (Fix 2) ──────────────────────

for filename in os.listdir("."):
    if filename.startswith("snapshot_") and filename.endswith(".json"):
        file_date_str = filename.replace("snapshot_", "").replace(".json", "")
        try:
            file_date = date.fromisoformat(file_date_str)
            if (date.today() - file_date).days > 3:
                os.remove(filename)
                log(f"🗑️  Cleaned up old snapshot: {filename}")
        except:
            pass
