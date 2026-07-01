import re
from datetime import datetime
from pathlib import Path

STATUS_START = "<!-- STATUS_SYNC:START -->"
STATUS_END = "<!-- STATUS_SYNC:END -->"


def _status_block(source):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"{STATUS_START}\n"
        f"<div class=\"status-sync\">Last updated: {timestamp} | Source: {source}</div>\n"
        f"{STATUS_END}"
    )


def update_project_status(path="project_status.html", source="manual"):
    page = Path(path)
    if not page.exists():
        return False

    text = page.read_text(encoding="utf-8")
    block = _status_block(source)

    pattern = re.compile(re.escape(STATUS_START) + r".*?" + re.escape(STATUS_END), re.DOTALL)
    if pattern.search(text):
        updated = pattern.sub(block, text, count=1)
    else:
        anchor = "<div class=\"tabs\">"
        if anchor in text:
            updated = text.replace(anchor, block + "\n\n" + anchor, 1)
        else:
            updated = text + "\n" + block + "\n"

    page.write_text(updated, encoding="utf-8")
    return True


if __name__ == "__main__":
    ok = update_project_status(source="manual run")
    print("project_status updated" if ok else "project_status not found")
