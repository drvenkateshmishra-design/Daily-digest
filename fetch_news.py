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


_IMG_TAG_RE = re.compile(r'<img[^>]+src="([^"]+)"')
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _extract_image(entry):
    """Best-effort image URL for an entry — checks the common RSS image
    mechanisms in order, returns None if the feed just doesn't have one."""
    thumbs = entry.get("media_thumbnail")
    if thumbs:
        return thumbs[0].get("url")
    media = entry.get("media_content")
    if media:
        for m in media:
            if not m.get("type") or m["type"].startswith("image"):
                if m.get("url"):
                    return m["url"]
    for enc in entry.get("enclosures", []):
        if enc.get("type", "").startswith("image") and enc.get("href"):
            return enc["href"]
    # Some feeds only put an <img> inline in the content/summary HTML.
    for field in ("content", "summary"):
        val = entry.get(field)
        if isinstance(val, list):  # feedparser wraps 'content' as a list of dicts
            val = val[0].get("value", "") if val else ""
        m = _IMG_TAG_RE.search(val or "")
        if m:
            return m.group(1)
    return None


def _best_raw_text(entry):
    """Some feeds (esp. blogs) put the FULL post in entry.content while
    summary stays a short teaser; others only populate summary. Use whichever
    is actually longer rather than assuming which field a given feed uses."""
    summary = entry.get("summary", "") or ""
    content_list = entry.get("content")
    content = content_list[0].get("value", "") if content_list else ""
    return content if len(content) > len(summary) else summary


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


def _fetch_feed_group(feeds_dict, max_age_hours, max_items_per_section, excerpt_max_chars):
    """Shared fetch/dedupe/trim logic used by both fetch_news() and
    fetch_blogs() — same shape, different config values (blogs post less
    often and get a much longer excerpt cap since full text is the point)."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    results = {}
    warnings = []

    for section, feed_urls in feeds_dict.items():
        all_items = []  # every entry fetched, regardless of age (used as fallback)
        for url in feed_urls:
            try:
                parsed = feedparser.parse(url)
                status = getattr(parsed, "status", None)
                if not parsed.entries:
                    # feedparser doesn't raise on HTTP errors (403, etc.) — it just
                    # comes back empty, so this is the only place that catches it.
                    reason = f"HTTP {status}" if status and status >= 400 else "0 entries returned"
                    msg = f"{section} — {url} — {reason}"
                    print(f"[news] WARNING: {msg} — check this feed")
                    warnings.append(msg)
                source_name = parsed.feed.get("title", url)
                for entry in parsed.entries:
                    all_items.append({
                        "title": entry.get("title", "Untitled").strip(),
                        "link": entry.get("link", ""),
                        "source": source_name,
                        "published": _entry_datetime(entry),
                        "excerpt": _clean_excerpt(_best_raw_text(entry), excerpt_max_chars),
                        "image": _extract_image(entry),
                    })
            except Exception as e:
                msg = f"{section} — {url} — error: {e}"
                print(f"[news] Skipping feed {url}: {e}")
                warnings.append(msg)

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

        results[section] = deduped[:max_items_per_section]

    return results, warnings


def fetch_news():
    """Returns (results, warnings) — see _fetch_feed_group."""
    return _fetch_feed_group(
        config.NEWS_FEEDS, config.NEWS_MAX_AGE_HOURS,
        config.MAX_NEWS_ITEMS_PER_SECTION, config.NEWS_EXCERPT_MAX_CHARS,
    )


def fetch_blogs():
    """Same shape as fetch_news() but for long-form blog sources — longer
    lookback window (blogs post less often), fewer items per section, much
    higher excerpt cap since these feeds actually carry full post text."""
    return _fetch_feed_group(
        config.BLOG_FEEDS,
        getattr(config, "BLOG_MAX_AGE_HOURS", 168),
        getattr(config, "MAX_BLOG_ITEMS_PER_SECTION", 3),
        getattr(config, "BLOG_EXCERPT_MAX_CHARS", 3000),
    )


if __name__ == "__main__":
    news, warnings = fetch_news()
    for section, items in news.items():
        print(f"\n=== {section} ({len(items)}) ===")
        for it in items:
            print(f"- {it['title']}  [{it['source']}]")
            if it["excerpt"]:
                print(f"    {it['excerpt'][:120]}...")
    if warnings:
        print(f"\n=== {len(warnings)} feed warning(s) ===")
        for w in warnings:
            print(f"! {w}")
