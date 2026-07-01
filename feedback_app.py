from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from news_connector import capture_news_feedback, get_news_preferences

HTML = """
<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Office Briefing Feedback</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 640px; margin: 40px auto; padding: 20px; }
    input, button { font-size: 16px; padding: 10px; margin-top: 8px; width: 100%; box-sizing: border-box; }
    button { cursor: pointer; }
    .note { color: #555; margin-top: 12px; }
  </style>
</head>
<body>
  <h1>News feedback</h1>
  <p>Tell the briefing system what topics matter to you.</p>
  <form method=\"post\" action=\"/feedback\">
    <label for=\"topics\">Topics (comma separated)</label>
    <input id=\"topics\" name=\"topics\" placeholder=\"property market, mortgage rates\" />
    <button type=\"submit\">Save feedback</button>
  </form>
  <div class=\"note\">Saved preferences will influence future news selection.</div>
</body>
</html>
"""


def _html_message(title, message):
    return f"""
<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 640px; margin: 40px auto; padding: 20px; }}
    a {{ display: inline-block; margin-top: 12px; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p>{message}</p>
  <a href=\"/\">Back to feedback form</a>
</body>
</html>
"""


class FeedbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))
            return

        if self.path.startswith("/vote"):
            try:
                query = self.path.split("?", 1)[1] if "?" in self.path else ""
                params = parse_qs(query)
                topic = params.get("topic", [""])[0].strip()
            except Exception:
                topic = ""

            if not topic:
                body = _html_message("Feedback not saved", "No topic was provided in the vote link.")
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(body.encode("utf-8"))
                return

            capture_news_feedback([topic], source="one-click")
            body = _html_message("Feedback saved", f"Saved topic preference: {topic}")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path != "/feedback":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        data = parse_qs(body)
        topics = data.get("topics", [""])[0]

        capture_news_feedback([topic for topic in topics.split(",") if topic.strip()], source="web")
        preferences = get_news_preferences().get("topics", {})
        message = "Saved topics: " + ", ".join(preferences.keys()) if preferences else "No topics were saved."
        payload = _html_message("Feedback saved", message).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        return


def run(host="127.0.0.1", port=8001):
    server = HTTPServer((host, port), FeedbackHandler)
    print(f"Feedback app running at http://{host}:{port}/")
    server.serve_forever()


if __name__ == "__main__":
    run()
