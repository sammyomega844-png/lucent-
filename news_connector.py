import os
import re
import csv
import sys
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

DEFAULT_NEWS_TOPICS = [
    "business market",
    "enterprise strategy",
    "supply chain risk",
    "technology adoption"
]
DEFAULT_MARKET_SYMBOLS = ["SPY", "DIA", "QQQ"]
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
PREFERENCE_FILE = Path("news_preferences.json")


def _preference_path():
    return Path(os.getenv("NEWS_PREFERENCE_FILE", str(PREFERENCE_FILE)))


def reset_news_preferences():
    path = _preference_path()
    if path.exists():
        path.unlink()


def _load_preferences():
    path = _preference_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_preferences(data):
    path = _preference_path()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def normalize_feedback_topics(topics):
    """Normalize a list of feedback topics into lowercase, deduped values."""
    if topics is None:
        return []
    normalized = []
    seen = set()
    for topic in topics:
        term = str(topic).strip().lower()
        if not term or term in seen:
            continue
        seen.add(term)
        normalized.append(term)
    return normalized


def record_news_feedback(topics, source="user"):
    """Persist positive feedback terms so later fetches can prioritize them."""
    prefs = _load_preferences()
    counts = prefs.setdefault("topics", {})
    for topic in normalize_feedback_topics(topics):
        counts[topic] = counts.get(topic, 0) + 1
    prefs["last_source"] = source
    _save_preferences(prefs)
    return prefs


def capture_news_feedback(topics=None, source="interactive"):
    """Capture feedback topics from a caller-provided list or an interactive prompt."""
    if topics is not None:
        normalized = [topic for topic in topics if str(topic).strip()]
        if normalized:
            return record_news_feedback(normalized, source=source)
        return _load_preferences()

    if os.getenv("NEWS_FEEDBACK_TOPICS"):
        normalized = [topic.strip() for topic in os.getenv("NEWS_FEEDBACK_TOPICS", "").split(",") if topic.strip()]
        if normalized:
            return record_news_feedback(normalized, source="env")
        return _load_preferences()

    if not hasattr(sys.stdin, "isatty") or not sys.stdin.isatty():
        return _load_preferences()

    try:
        raw = input("News feedback: enter relevant topics for future briefings (comma-separated, blank to skip): ").strip()
    except (EOFError, OSError):
        return _load_preferences()

    normalized = [topic.strip() for topic in raw.split(",") if topic.strip()]
    if not normalized:
        return _load_preferences()
    return record_news_feedback(normalized, source=source)


def record_quick_feedback(action, topics=None, source="quick"):
    """Record a simple positive/negative action as feedback using optional topic hints."""
    if action not in {"thumbs_up", "thumbs_down", "relevant", "not_relevant"}:
        return _load_preferences()

    topic_list = []
    if topics:
        topic_list.extend(normalize_feedback_topics(topics))

    if action in {"thumbs_up", "relevant"}:
        if not topic_list:
            topic_list = ["general business"]
        return record_news_feedback(topic_list, source=source)

    if action in {"thumbs_down", "not_relevant"}:
        return record_news_feedback(topic_list or ["irrelevant"], source=source)

    return _load_preferences()


def get_news_preferences():
    return _load_preferences()


def _dedupe(items):
    seen = set()
    out = []
    for item in items:
        if not item:
            continue
        item_clean = item.strip()
        if item_clean.lower() in seen:
            continue
        seen.add(item_clean.lower())
        out.append(item_clean)
    return out


def build_news_topics():
    """Build a tailored topic list from explicit overrides or a user profile."""
    env_topics = os.getenv("NEWS_TOPICS", "").strip()
    if env_topics:
        return _dedupe([topic.strip() for topic in env_topics.split(";") if topic.strip()])

    user_industry = os.getenv("USER_INDUSTRY", "").strip()
    user_region = os.getenv("USER_REGION", "").strip()
    user_interests = [interest.strip() for interest in os.getenv("USER_INTERESTS", "").split(",") if interest.strip()]

    prefs = get_news_preferences().get("topics", {})
    weighted_topics = []
    for topic, count in prefs.items():
        if count > 0:
            weighted_topics.extend([topic] * min(count, 3))

    topics = []
    if user_industry:
        topics.append(user_industry)
        if user_region:
            topics.append(f"{user_industry} {user_region}")
            topics.append(f"{user_industry} market {user_region}")
        topics.append(f"{user_industry} market")

    if user_region:
        topics.append(user_region)
        topics.append(f"{user_region} property market")
        topics.append(f"real estate {user_region}")

    for interest in user_interests:
        topics.append(interest)
        if user_region:
            topics.append(f"{interest} {user_region}")
        if user_industry:
            topics.append(f"{interest} {user_industry}")

    topics.extend(weighted_topics)
    topics.extend(DEFAULT_NEWS_TOPICS)
    return _dedupe(topics)


def build_profile_terms():
    """Create simple keyword terms from the current user profile."""
    user_industry = os.getenv("USER_INDUSTRY", "").strip().lower()
    user_region = os.getenv("USER_REGION", "").strip().lower()
    user_interests = [interest.strip().lower() for interest in os.getenv("USER_INTERESTS", "").split(",") if interest.strip()]
    terms = []
    if user_industry:
        terms.append(user_industry)
    if user_region:
        terms.append(user_region)
    terms.extend(user_interests)
    return _dedupe(terms)


def get_news_context_summary():
    """Create a compact summary that explains how news selection is being tailored."""
    user_industry = os.getenv("USER_INDUSTRY", "").strip()
    user_region = os.getenv("USER_REGION", "").strip()
    user_interests = [interest.strip() for interest in os.getenv("USER_INTERESTS", "").split(",") if interest.strip()]

    profile_parts = []
    if user_industry:
        profile_parts.append(f"industry={user_industry}")
    if user_region:
        profile_parts.append(f"region={user_region}")
    if user_interests:
        profile_parts.append(f"interests={', '.join(user_interests)}")

    prefs = get_news_preferences().get("topics", {})
    learned_terms = [term for term, count in sorted(prefs.items(), key=lambda item: item[1], reverse=True) if count > 0][:5]
    context_parts = []
    if profile_parts:
        context_parts.append("profile=" + "; ".join(profile_parts))
    if learned_terms:
        context_parts.append("learned_preferences=" + ", ".join(learned_terms))

    if not context_parts:
        return "News context: general business coverage."
    return "News context: " + "; ".join(context_parts) + "."


def _matches_profile(article, profile_terms):
    if not profile_terms:
        return True
    haystack = " ".join([
        article.get("title", ""),
        article.get("description", ""),
        article.get("topic", "")
    ]).lower()
    return any(term.lower() in haystack for term in profile_terms)


def _fetch_url(url, timeout=15):
    request = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close"
    })
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def _parse_rss(xml_text, max_items=6):
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    items = []
    for item in root.findall(".//item")[:max_items]:
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        description = item.findtext("description", "").strip()
        pub_date = item.findtext("pubDate", "").strip()
        source = item.findtext("source", "").strip()
        items.append({
            "title": title,
            "link": link,
            "description": description,
            "published": pub_date,
            "source": source or "Google News"
        })
    return items


def _google_news_rss(query):
    params = urllib.parse.urlencode({
        "q": query,
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en"
    })
    return f"https://news.google.com/rss/search?{params}"


def fetch_news(topics=None, max_articles=6):
    """Fetch the latest business news headlines from Google News RSS feeds."""
    if topics is None:
        topics = build_news_topics()

    articles = []
    seen_titles = set()
    profile_terms = build_profile_terms()

    for topic in topics:
        try:
            feed_url = _google_news_rss(topic)
            xml_text = _fetch_url(feed_url)
            feed_articles = _parse_rss(xml_text, max_items=max_articles * 2)
        except Exception:
            continue

        for article in feed_articles:
            if article["title"] in seen_titles:
                continue
            if profile_terms and not _matches_profile(article, profile_terms):
                continue
            seen_titles.add(article["title"])
            article["topic"] = topic
            articles.append(article)
            if len(articles) >= max_articles:
                break

        if len(articles) >= max_articles:
            break

    if not articles:
        return fetch_news(topics=DEFAULT_NEWS_TOPICS, max_articles=max_articles)

    return articles


def _parse_quote_response(raw):
    try:
        data = json.loads(raw)
    except Exception:
        return []

    results = data.get("quoteResponse", {}).get("result", [])
    entries = []
    for quote in results:
        price = quote.get("regularMarketPrice")
        if price is None:
            price = quote.get("regularMarketPreviousClose")

        if price is None:
            continue

        entries.append({
            "symbol": quote.get("symbol", ""),
            "shortName": quote.get("shortName", quote.get("symbol", "")),
            "price": price,
            "change": quote.get("regularMarketChange", 0.0),
            "changePercent": quote.get("regularMarketChangePercent", 0.0),
            "marketState": quote.get("marketState", ""),
            "time": datetime.fromtimestamp(quote.get("regularMarketTime", 0)).isoformat() if quote.get("regularMarketTime") else ""
        })

    return entries


def _fetch_market_quotes(query):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={urllib.parse.quote(query)}"
        raw = _fetch_url(url)
        return _parse_quote_response(raw)
    except Exception:
        return []


def _fetch_yahoo_html(symbol):
    try:
        url = f"https://finance.yahoo.com/quote/{urllib.parse.quote(symbol)}"
        html = _fetch_url(url)
        price_match = re.search(r'<fin-streamer[^>]+data-field="regularMarketPrice"[^>]+data-value="([0-9.,+-]+)"', html)
        change_match = re.search(r'<fin-streamer[^>]+data-field="regularMarketChange"[^>]+data-value="([0-9.,+-]+)"', html)
        pct_match = re.search(r'<fin-streamer[^>]+data-field="regularMarketChangePercent"[^>]+data-value="([0-9.,+-]+)"', html)
        if not price_match:
            return None

        price = float(price_match.group(1).replace(",", ""))
        change = float(change_match.group(1).replace(",", "")) if change_match else 0.0
        pct = float(pct_match.group(1).replace(",", "")) if pct_match else 0.0
        return {
            "symbol": symbol,
            "shortName": symbol,
            "price": price,
            "change": change,
            "changePercent": pct,
            "marketState": "OPEN",
            "time": datetime.utcnow().isoformat()
        }
    except Exception:
        return None


def _fetch_alphavantage_quote(symbol, api_key):
    try:
        url = (
            f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
            f"&symbol={urllib.parse.quote(symbol)}&apikey={urllib.parse.quote(api_key)}"
        )
        raw = _fetch_url(url)
        data = json.loads(raw)
        quote = data.get("Global Quote", {})
        price = quote.get("05. price")
        if price is None:
            return None

        change = quote.get("09. change", "0")
        change_percent = quote.get("10. change percent", "0%")

        return {
            "symbol": symbol,
            "shortName": symbol,
            "price": float(price),
            "change": float(change),
            "changePercent": float(change_percent.replace("%", "")),
            "marketState": "OPEN",
            "time": quote.get("07. latest trading day", "")
        }
    except Exception:
        return None


def _fetch_alphavantage_quotes(symbols, api_key):
    entries = []
    for symbol in symbols:
        quote = _fetch_alphavantage_quote(symbol, api_key)
        if quote:
            entries.append(quote)
    return entries


def _fetch_market_quotes_stooq(symbols):
    try:
        entries = []
        for symbol in symbols:
            query_symbol = symbol.replace("^", "").strip().lower()
            if not query_symbol:
                continue

            url = f"https://stooq.com/q/l/?s={urllib.parse.quote(query_symbol)}&f=sd2t2ohlcv&h&e=csv"
            raw = _fetch_url(url)
            lines = raw.strip().splitlines()
            if len(lines) < 2:
                continue

            reader = csv.DictReader(lines)
            for row in reader:
                symbol_value = row.get("Symbol", "").strip()
                close = row.get("Close", "").strip()
                open_price = row.get("Open", "").strip()
                if not close or close == "N/A":
                    continue

                price = float(close)
                change = None
                change_percent = None
                if open_price and open_price != "N/A":
                    open_val = float(open_price)
                    change = price - open_val
                    change_percent = (change / open_val * 100) if open_val != 0 else 0

                entries.append({
                    "symbol": symbol_value.upper() if symbol_value else symbol.upper(),
                    "shortName": symbol_value.upper() if symbol_value else symbol.upper(),
                    "price": price,
                    "change": change,
                    "changePercent": change_percent,
                    "marketState": "CLOSED",
                    "time": datetime.utcnow().isoformat()
                })

        return entries
    except Exception:
        return []


def fetch_market_data(symbols=None):
    """Fetch a small market pulse for major index symbols using free public feeds."""
    if symbols is None:
        symbols = DEFAULT_MARKET_SYMBOLS

    symbols = [s.strip() for s in symbols if s.strip()]
    if not symbols:
        symbols = DEFAULT_MARKET_SYMBOLS

    alpha_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")

    # Primary free attempt: Stooq per symbol feed
    entries = _fetch_market_quotes_stooq(symbols)
    if entries:
        return entries

    # Secondary free attempt: Yahoo quote API
    entries = _fetch_market_quotes(",".join(symbols))
    if entries:
        return entries

    # Third fallback: Yahoo HTML scrape per symbol
    fallback = []
    for symbol in symbols:
        quote = _fetch_yahoo_html(symbol)
        if quote:
            fallback.append(quote)
        if len(fallback) >= len(symbols):
            break

    if fallback:
        return fallback

    # Last resort: Alphavantage for any available symbols
    fallback = []
    for symbol in symbols:
        quote = _fetch_alphavantage_quote(symbol, alpha_key)
        if quote:
            fallback.append(quote)
        if len(fallback) >= len(symbols):
            break

    return fallback


def format_news_for_ai(articles):
    if not articles:
        return "No news stories were available from the configured feeds."

    lines = ["Latest business headlines and themes:"]
    for i, article in enumerate(articles, start=1):
        title = article.get("title", "(no title)")
        source = article.get("source", "Unknown source")
        topic = article.get("topic", "business")
        description = article.get("description", "").replace("\n", " ").strip()
        lines.append(f"NEWS {i}: {title}")
        lines.append(f"  Topic: {topic}")
        lines.append(f"  Source: {source}")
        if description:
            lines.append(f"  Summary: {description[:260]}")
        if article.get("link"):
            lines.append(f"  Link: {article['link']}")
        lines.append("")

    return "\n".join(lines)


def format_market_for_ai(entries):
    if not entries:
        return "No market pulse data could be fetched at this time."

    lines = ["Market pulse:"]
    for item in entries:
        symbol = item.get("symbol", "")
        name = item.get("shortName", symbol)
        price = item.get("price")
        change = item.get("change")
        percent = item.get("changePercent")
        market_state = item.get("marketState", "")
        if price is None:
            continue
        change_str = f"{change:+.2f}" if change is not None else "N/A"
        percent_str = f"{percent:+.2f}%" if percent is not None else "N/A"
        lines.append(f"{name} ({symbol}): {price:.2f} {change_str} ({percent_str}) — {market_state}")
    return "\n".join(lines)


def summarize_market_pulse(entries):
    if not entries:
        return "No market pulse data is available at this time."

    positives = [e for e in entries if e.get("changePercent", 0) > 0]
    negatives = [e for e in entries if e.get("changePercent", 0) < 0]
    neutral = [e for e in entries if e.get("changePercent", 0) == 0]

    best = max(entries, key=lambda e: e.get("changePercent", 0))
    worst = min(entries, key=lambda e: e.get("changePercent", 0))

    summary = []
    if len(positives) == len(entries):
        summary.append("The market pulse is positive across the tracked indices.")
    elif len(negatives) == len(entries):
        summary.append("The market pulse is negative across the tracked indices.")
    else:
        summary.append("The market pulse is mixed: some indices are up while others are down.")

    summary.append(f"Top mover: {best.get('symbol', '')} {best.get('changePercent', 0):+.2f}%.")
    summary.append(f"Largest drag: {worst.get('symbol', '')} {worst.get('changePercent', 0):+.2f}%.")

    if abs(best.get('changePercent', 0)) >= 0.8 or abs(worst.get('changePercent', 0)) >= 0.8:
        summary.append("This suggests a stronger near-term market signal that should influence priorities.")

    return " ".join(summary)


def load_news_and_market(max_articles=6):
    topics = build_news_topics()

    market_symbols = os.getenv("MARKET_SYMBOLS")
    if market_symbols:
        symbols = [symbol.strip() for symbol in market_symbols.split(",") if symbol.strip()]
    else:
        symbols = DEFAULT_MARKET_SYMBOLS

    news = fetch_news(topics=topics, max_articles=max_articles)
    market = fetch_market_data(symbols=symbols)

    return news, market
