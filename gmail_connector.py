# ============================================================
# GMAIL CONNECTOR — Session 6
# Connects to Gmail API, reads recent emails,
# extracts what matters for the morning briefing
# ============================================================

import os
import base64
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ── Scopes ───────────────────────────────────────────────────
# readonly = we can only READ emails, never send or delete

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

TOKEN_FILE       = "gmail_token.json"
CREDENTIALS_FILE = "credentials.json"

def get_gmail_service():
    """
    Authenticate with Gmail API.
    First run: opens browser for you to log in and grant access.
    All future runs: uses saved token automatically.
    """
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_email_body(msg):
    """Extract plain text body from a Gmail message"""
    body = ""
    try:
        payload = msg.get("payload", {})

        if "body" in payload and payload["body"].get("data"):
            data = payload["body"]["data"]
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

        elif "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data", "")
                    if data:
                        body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                        break
    except Exception:
        pass

    return body[:2000].strip()


def fetch_recent_emails(hours_back=24, max_emails=20):
    """
    Fetch emails from the last X hours.
    Returns a list of email summaries ready for AI processing.
    Excludes promotions and social notifications automatically.
    """
    try:
        service = get_gmail_service()
    except Exception as e:
        return [], f"Gmail connection error: {e}"

    since = datetime.utcnow() - timedelta(hours=hours_back)
    since_timestamp = int(since.timestamp())
    query = f"after:{since_timestamp} -category:promotions -category:social"

    try:
        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_emails
        ).execute()
    except Exception as e:
        return [], f"Gmail API error: {e}"

    messages = results.get("messages", [])

    if not messages:
        return [], None

    emails = []
    for msg_ref in messages:
        try:
            msg = service.users().messages().get(
                userId="me",
                id=msg_ref["id"],
                format="full"
            ).execute()

            headers = {
                h["name"]: h["value"]
                for h in msg.get("payload", {}).get("headers", [])
            }

            sender  = headers.get("From", "Unknown")
            subject = headers.get("Subject", "(no subject)")
            date_str= headers.get("Date", "")
            body    = get_email_body(msg)

            if len(body) < 30:
                continue

            emails.append({
                "sender":  sender,
                "subject": subject,
                "date":    date_str,
                "body":    body,
                "snippet": msg.get("snippet", "")
            })

        except Exception:
            continue

    return emails, None


def format_emails_for_ai(emails):
    """Format email list into structured text for AI analysis"""
    if not emails:
        return "No emails requiring attention in the last 24 hours."

    lines = []
    for i, email in enumerate(emails, 1):
        lines.append(f"EMAIL {i}:")
        lines.append(f"  From: {email['sender']}")
        lines.append(f"  Subject: {email['subject']}")
        lines.append(f"  Preview: {email['snippet'][:200]}")
        if email['body']:
            lines.append(f"  Content: {email['body'][:500]}")
        lines.append("")

    return "\n".join(lines)


# ── Standalone test ───────────────────────────────────────────

if __name__ == "__main__":
    print("🔐 Connecting to Gmail...")
    print("   A browser window will open — log in and click Allow")
    print()

    emails, error = fetch_recent_emails(hours_back=24, max_emails=10)

    if error:
        print(f"❌ Error: {error}")
    else:
        print(f"✅ Connected to Gmail successfully")
        print(f"📧 Found {len(emails)} emails in the last 24 hours\n")

        for i, email in enumerate(emails, 1):
            print(f"  {i}. {email['subject']}")
            print(f"     From: {email['sender']}")
            print(f"     Preview: {email['snippet'][:100]}...")
            print()

        if not emails:
            print("   No emails found — inbox clear or all filtered as promotions/social")
