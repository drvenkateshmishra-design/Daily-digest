"""Tracks which news/blog items have already appeared in a past digest, so
the same article doesn't get repeated day after day when a feed goes quiet
(this happens more than you'd think — fetch_news.py's age-window fallback
deliberately shows the most recent items even if nothing new was published,
"better slightly stale than blank" — which is good for never having an
empty section, but means the same top story can otherwise repeat for days).

Persisted as a small JSON file in the repo (seen_items.json) — GitHub
Actions runs are otherwise fully stateless between days, so something has
to commit this back to the repo after each run for it to survive to
tomorrow. See daily-digest.yml for the commit step, and main.py for how
this gets loaded/used/saved.

Only NEWS_FEEDS/BLOG_FEEDS items go through this. Journal articles from
PubMed already sort by publication date each day so repeats are naturally
rare there; Thoughts-for-the-Day and Ek Kavita Roj are date-seeded picks
from a fixed local pool with no live fetching at all, so there's nothing
to repeat in the first place.
"""
import json
import os
from datetime import date, datetime, timedelta

SEEN_FILE = os.path.join(os.path.dirname(__file__), "seen_items.json")
PRUNE_AFTER_DAYS = 30  # forget items older than this so the file doesn't grow forever


def item_key(item):
    """A stable identity for one news/blog item — the link, since it's
    unique and (unlike title) won't collide across unrelated stories. Falls
    back to a normalized title for the rare item with no link at all."""
    link = (item.get("link") or "").strip()
    if link:
        return link
    return "title:" + item.get("title", "").strip().lower()


def load_seen(path=SEEN_FILE):
    """Returns {item_key: "YYYY-MM-DD first seen"}. Empty dict if the file
    doesn't exist yet (first run ever) or fails to parse (never let a
    corrupt state file break the whole pipeline — just start fresh)."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[seen_store] couldn't read {path}, starting fresh: {e}")
        return {}


def save_seen(seen, path=SEEN_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=1, sort_keys=True)


def _parse_date(iso_date_str):
    try:
        return datetime.strptime(iso_date_str, "%Y-%m-%d").date()
    except Exception:
        return date.min


def prune(seen, max_age_days=PRUNE_AFTER_DAYS):
    """Drop entries older than max_age_days — an item that hasn't recurred
    in a month is never going to, no reason to keep the file growing forever."""
    cutoff = date.today() - timedelta(days=max_age_days)
    return {k: v for k, v in seen.items() if _parse_date(v) >= cutoff}


def mark_seen(seen, sections_dict):
    """sections_dict: {section_name: [items]} — the shape fetch_news()/
    fetch_blogs() return. Records every item actually shown today. Mutates
    seen in place and also returns it, for chaining."""
    today_str = date.today().isoformat()
    for items in sections_dict.values():
        for it in items:
            seen[item_key(it)] = today_str
    return seen
