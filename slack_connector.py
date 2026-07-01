"""
Slack Channel Monitor - Free tier integration
Reads recent messages from designated Slack channels
Extracts decisions, action items, unresolved threads
No paid APIs - uses free Slack OAuth + read permissions
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    WebClient = None


def get_slack_client():
    """Initialize Slack client from environment token."""
    if not WebClient:
        return None
    token = os.getenv("SLACK_BOT_TOKEN", "").strip()
    if not token:
        return None
    return WebClient(token=token)


def list_channels(client):
    """List all public channels the bot has access to."""
    if not client:
        return []
    try:
        result = client.conversations_list(types="public_channel", limit=50)
        return [{"id": c["id"], "name": c["name"]} for c in result.get("channels", [])]
    except SlackApiError:
        return []


def read_channel_messages(client, channel_id, hours_back=24):
    """Read recent messages from a channel."""
    if not client:
        return []
    try:
        oldest = (datetime.now() - timedelta(hours=hours_back)).timestamp()
        result = client.conversations_history(channel=channel_id, oldest=oldest, limit=50)
        messages = []
        for msg in result.get("messages", []):
            text = msg.get("text", "").strip()
            if text and not msg.get("bot_id") and not text.startswith("_"):
                messages.append({
                    "timestamp": msg.get("ts"),
                    "user": msg.get("user", "unknown"),
                    "text": text,
                    "thread_ts": msg.get("thread_ts"),
                })
        return messages
    except SlackApiError:
        return []


def extract_action_items(messages):
    """Extract potential action items from messages."""
    action_keywords = ["todo", "action item", "assigned to", "due", "needs", "urgent", "asap", "blocked"]
    items = []
    for msg in messages:
        text_lower = msg["text"].lower()
        if any(kw in text_lower for kw in action_keywords):
            items.append({"user": msg["user"], "text": msg["text"][:200]})
    return items[:5]


def extract_decisions(messages):
    """Extract messages indicating decisions were made."""
    decision_keywords = ["decided", "we will", "approved", "commit to", "going with", "chose"]
    decisions = []
    for msg in messages:
        text_lower = msg["text"].lower()
        if any(kw in text_lower for kw in decision_keywords):
            decisions.append({"user": msg["user"], "text": msg["text"][:200]})
    return decisions[:5]


def count_threaded_discussions(messages):
    """Count unresolved threaded discussions."""
    threaded = [m for m in messages if m.get("thread_ts")]
    return len(threaded)


def load_channel_config():
    """Load Slack channel configuration."""
    config_path = Path("slack_channels.json")
    if config_path.exists():
        try:
            return json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_channel_config(config):
    """Save Slack channel configuration."""
    Path("slack_channels.json").write_text(json.dumps(config, indent=2), encoding="utf-8")


def build_slack_context(monitored_channels=None):
    """Build team context from Slack channels."""
    client = get_slack_client()
    if not client:
        return "Slack API not configured (set SLACK_BOT_TOKEN to enable team context)."

    if monitored_channels is None:
        config = load_channel_config()
        monitored_channels = config.get("channels", [])

    if not monitored_channels:
        return "No Slack channels configured. Add channels to slack_channels.json."

    context_lines = ["SLACK TEAM CONTEXT (Last 24 hours):"]

    for channel_name in monitored_channels:
        channels = list_channels(client)
        channel = next((c for c in channels if c["name"] == channel_name), None)
        if not channel:
            context_lines.append(f"  ⚠️ Channel #{channel_name} not found or no access.")
            continue

        messages = read_channel_messages(client, channel["id"], hours_back=24)
        if not messages:
            continue

        context_lines.append(f"\n  📌 #{channel_name}:")
        actions = extract_action_items(messages)
        if actions:
            context_lines.append(f"    Action items: {len(actions)} found")
            for action in actions[:2]:
                context_lines.append(f"      • {action['text'][:100]}...")

        decisions = extract_decisions(messages)
        if decisions:
            context_lines.append(f"    Decisions made: {len(decisions)} found")
            for decision in decisions[:2]:
                context_lines.append(f"      ✓ {decision['text'][:100]}...")

        threads = count_threaded_discussions(messages)
        if threads > 0:
            context_lines.append(f"    Unresolved threads: {threads}")

    return "\n".join(context_lines)


def configure_channels_interactive():
    """Interactive setup for monitored channels."""
    client = get_slack_client()
    if not client:
        print("❌ SLACK_BOT_TOKEN not set. Set the environment variable and retry.")
        return

    print("🔍 Fetching available channels...")
    channels = list_channels(client)
    if not channels:
        print("❌ No channels found. Check bot permissions.")
        return

    print(f"\n✅ Found {len(channels)} channels:")
    for i, ch in enumerate(channels[:20], 1):
        print(f"  {i}. #{ch['name']}")

    if len(channels) > 20:
        print(f"  ... and {len(channels) - 20} more")

    selected = input("\nEnter channel names to monitor (comma-separated, e.g. 'general,projects,sales'): ").strip()
    if not selected:
        print("No channels selected.")
        return

    channel_list = [c.strip() for c in selected.split(",")]
    config = {"channels": channel_list, "last_updated": datetime.now().isoformat()}
    save_channel_config(config)
    print(f"✅ Configured {len(channel_list)} channels: {', '.join(channel_list)}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        configure_channels_interactive()
    else:
        context = build_slack_context()
        print(context)
