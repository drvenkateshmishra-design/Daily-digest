"""Fetches and filters recent items from configured RSS feeds."""
import feedparser
from datetime import datetime, timezone, timedelta
from time import mktime

import config


def _entry_datetime(entry):
    for key in ("published_parsed", "updated_parsed"):
        val = entry.get(key)
        if val:
            return datetime.fromtimestamp(mktime(val), tz=timezone.utc)
    return None


def fetch_news():
    """Returns dict: {section_name: [ {title, link, source, published} ]}"""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=config.NEWS_MAX_AGE_HOURS)
    results = {}

    for section, feed_urls in config.NEWS_FEEDS.items():
        all_items = []  # every entry fetched, regardless of age (used as fallback)
        for url in feed_urls:
            try:
                parsed = feedparser.parse(url)
                source_name = parsed.feed.get("title", url)
                for entry in parsed.entries:
                    all_items.append({
                        "title": entry.get("title", "Untitled").strip(),
                        "link": entry.get("link", ""),
                        "source": source_name,
                        "published": _entry_datetime(entry),
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
