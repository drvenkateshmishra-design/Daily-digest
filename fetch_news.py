"""Fetches and filters recent items from configured RSS feeds."""
import feedparser
import re
import html as html_lib
from datetime import datetime, timezone, timedelta
from time import mktime
import config


def _entry_datetime(entry):
    for key in ("published_parsed", "updated_parsed"):
        val = entry.get(key)
        if val:
            return datetime.fromtimestamp(mktime(val), tz=timezone.utc)
    return None


_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _clean_excerpt(raw, max_chars=None):
    """Strip HTML, decode entities, collapse whitespace, truncate on a word
    boundary. Uses whatever summary the feed itself provides — no scraping,
    no fetching the article page, so it works the same whether the source
    is open or paywalled."""
    if not raw:
        return ""
    max_chars = max_chars or getattr(config, "NEWS_EXCERPT_MAX_CHARS", 500)
    text = _TAG_RE.sub(" ", raw)
    text = html_lib.unescape(text)
    text = _WS_RE.sub(" ", text).strip()
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars].rsplit(" ", 1)[0]
    return truncated.rstrip(".,;: ") + "…"


def fetch_news():
    """Returns dict: {section_name: [ {title, link, source, published, excerpt} ]}"""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=config.NEWS_MAX_AGE_HOURS)
    results = {}

    for section, feed_urls in config.NEWS_FEEDS.items():
        all_items = []  # every entry fetched, regardless of age (used as fallback)
        for url in feed_urls:
            try:
                parsed = feedparser.parse(url)
                status = getattr(parsed, "status", None)
                if not parsed.entries:
                    # feedparser doesn't raise on HTTP errors (403, etc.) — it just
                    # comes back empty, so this is the only place that catches it.
                    reason = f"HTTP {status}" if status and status >= 400 else "0 entries returned"
                    print(f"[news] WARNING: {section} — {url} — {reason} — check this feed")
                source_name = parsed.feed.get("title", url)
                for entry in parsed.entries:
                    raw_summary = entry.get("summary") or entry.get("description", "")
                    all_items.append({
                        "title": entry.get("title", "Untitled").strip(),
                        "link": entry.get("link", ""),
                        "source": source_name,
                        "published": _entry_datetime(entry),
                        "excerpt": _clean_excerpt(raw_summary),
                    })
            except Exception as e:
                print(f"[news] Skipping feed {url}: {e}")

        def _dedupe_sorted(items):
            items = sorted(items, key=lambda x: x["published"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
            seen, out = set(), []
            for it in items:
                key = it["title"].lower()
                if key in seen:
                    continue
                seen.add(key)
                out.append(it)
            return out

        recent = [it for it in all_items if not it["published"] or it["published"] >= cutoff]
        deduped = _dedupe_sorted(recent)
        if not deduped:
            # Fallback: nothing in the age window — show the most recent items anyway
            # so the section isn't empty (better slightly stale than blank).
            deduped = _dedupe_sorted(all_items)

        results[section] = deduped[:config.MAX_NEWS_ITEMS_PER_SECTION]

    return results


if __name__ == "__main__":
    news = fetch_news()
    for section, items in news.items():
        print(f"\n=== {section} ({len(items)}) ===")
        for it in items:
            print(f"- {it['title']}  [{it['source']}]")
            if it["excerpt"]:
                print(f"    {it['excerpt'][:120]}...")
