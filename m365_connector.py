"""
Microsoft 365 Connector - Free Microsoft Graph API integration
Reads Outlook emails, Teams messages, calendar events, OneDrive files
No paid APIs - uses free Microsoft Graph + OAuth device flow
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    requests = None


class M365Client:
    """Microsoft 365 Graph API client."""

    def __init__(self, token=None):
        self.token = token or os.getenv("M365_ACCESS_TOKEN", "").strip()
        self.base_url = "https://graph.microsoft.com/v1.0"

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def is_configured(self):
        return bool(self.token) and requests is not None

    def get_recent_emails(self, hours_back=24, limit=10):
        """Fetch recent emails from inbox."""
        if not self.is_configured():
            return []

        try:
            cutoff = (datetime.utcnow() - timedelta(hours=hours_back)).isoformat() + "Z"
            url = f"{self.base_url}/me/mailfolders/inbox/messages"
            params = {
                "$filter": f"receivedDateTime ge {cutoff}",
                "$top": limit,
                "$orderby": "receivedDateTime desc",
            }
            resp = requests.get(url, headers=self._headers(), params=params, timeout=10)
            if resp.status_code == 200:
                messages = []
                for msg in resp.json().get("value", []):
                    messages.append({
                        "from": msg.get("from", {}).get("emailAddress", {}).get("name", "Unknown"),
                        "subject": msg.get("subject", ""),
                        "timestamp": msg.get("receivedDateTime", ""),
                    })
                return messages
        except Exception:
            pass
        return []

    def get_calendar_events(self, hours_back=24, limit=10):
        """Fetch recent calendar events."""
        if not self.is_configured():
            return []

        try:
            cutoff = (datetime.utcnow() - timedelta(hours=hours_back)).isoformat()
            url = f"{self.base_url}/me/events"
            params = {
                "$filter": f"start/dateTime ge '{cutoff}'",
                "$top": limit,
                "$orderby": "start/dateTime",
            }
            resp = requests.get(url, headers=self._headers(), params=params, timeout=10)
            if resp.status_code == 200:
                events = []
                for evt in resp.json().get("value", []):
                    events.append({
                        "subject": evt.get("subject", ""),
                        "start": evt.get("start", {}).get("dateTime", ""),
                        "attendees": len(evt.get("attendees", [])),
                    })
                return events
        except Exception:
            pass
        return []

    def get_teams_messages(self, team_id, channel_id, hours_back=24, limit=20):
        """Fetch recent Teams messages from a specific channel."""
        if not self.is_configured() or not team_id or not channel_id:
            return []

        try:
            cutoff = (datetime.utcnow() - timedelta(hours=hours_back)).isoformat() + "Z"
            url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages"
            params = {
                "$filter": f"createdDateTime ge {cutoff}",
                "$top": limit,
            }
            resp = requests.get(url, headers=self._headers(), params=params, timeout=10)
            if resp.status_code == 200:
                messages = []
                for msg in resp.json().get("value", []):
                    body = msg.get("body", {}).get("content", "")
                    if body and body != "<br/>":
                        messages.append({
                            "from": msg.get("from", {}).get("user", {}).get("displayName", "Unknown"),
                            "text": body[:200],
                            "timestamp": msg.get("createdDateTime", ""),
                        })
                return messages
        except Exception:
            pass
        return []

    def get_onedrive_recent_files(self, hours_back=24, limit=5):
        """Fetch recently modified OneDrive files."""
        if not self.is_configured():
            return []

        try:
            cutoff = (datetime.utcnow() - timedelta(hours=hours_back)).isoformat() + "Z"
            url = f"{self.base_url}/me/drive/recent"
            resp = requests.get(url, headers=self._headers(), timeout=10)
            if resp.status_code == 200:
                files = []
                for item in resp.json().get("value", [])[:limit]:
                    if item.get("lastModifiedDateTime"):
                        mod_time = item["lastModifiedDateTime"]
                        if mod_time > cutoff:
                            files.append({
                                "name": item.get("name", ""),
                                "modified": mod_time,
                            })
                return files
        except Exception:
            pass
        return []


def load_m365_config():
    """Load M365 configuration."""
    config_path = Path("m365_config.json")
    if config_path.exists():
        try:
            return json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_m365_config(config):
    """Save M365 configuration."""
    Path("m365_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")


def build_m365_context():
    """Build enterprise context from Microsoft 365."""
    client = M365Client()
    if not client.is_configured():
        return "Microsoft 365 not configured (set M365_ACCESS_TOKEN to enable enterprise context)."

    context_lines = ["MICROSOFT 365 CONTEXT (Last 24 hours):"]

    emails = client.get_recent_emails(hours_back=24, limit=5)
    if emails:
        context_lines.append(f"\n  📧 Recent emails: {len(emails)} received")
        for email in emails[:3]:
            context_lines.append(f"    From {email['from']}: {email['subject'][:80]}...")

    events = client.get_calendar_events(hours_back=24, limit=10)
    if events:
        context_lines.append(f"\n  📅 Upcoming events: {len(events)} scheduled")
        for evt in events[:3]:
            context_lines.append(f"    {evt['subject']} ({evt['attendees']} attendees)")

    files = client.get_onedrive_recent_files(hours_back=24, limit=5)
    if files:
        context_lines.append(f"\n  📁 Recently modified files: {len(files)}")
        for file in files[:3]:
            context_lines.append(f"    {file['name']}")

    config = load_m365_config()
    if config.get("teams"):
        for team_channel in config["teams"][:2]:
            team_id = team_channel.get("team_id")
            channel_id = team_channel.get("channel_id")
            messages = client.get_teams_messages(team_id, channel_id, hours_back=24, limit=10)
            if messages:
                context_lines.append(f"\n  💬 Teams activity: {len(messages)} messages")

    return "\n".join(context_lines)


def save_token(token):
    """Save token to environment variable instructions (user must set manually)."""
    print(f"✅ Token received. Add to your environment:")
    print(f"   set M365_ACCESS_TOKEN={token[:20]}... (full token)")
    print("\nOr add to .env file:")
    print(f"   M365_ACCESS_TOKEN={token}")


if __name__ == "__main__":
    context = build_m365_context()
    print(context)
