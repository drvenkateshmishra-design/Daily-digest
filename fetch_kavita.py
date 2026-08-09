"""Standalone utility for regenerating config.py's KAVITA_ROJ_POEMS pool.

NOT imported by main.py anymore — see config.py's comment above
KAVITA_ROJ_POEMS for why: GitHub Actions runner IPs get a blanket 403 from
kavitakosh.org (confirmed live, 8/8 attempts, while the identical request
works fine from other environments — this is IP-range blocking on their
end, not anything wrong with the request itself; the same run also hit a
403 on two unrelated Substack feeds, confirming it's about where the
request comes from, not what it contains). A live per-day call would just
fail every time the pipeline actually runs. So the daily pick now comes
from a pre-verified static pool in config.py instead (same pattern as the
Sanskrit/English/Hindi quotes, which never touch the network at all).

Run this file directly, from a machine/network that ISN'T IP-blocked, to
regenerate or grow that pool — it prints one JSON poem per success and you
can pipe/collect the output. Not run automatically by anything.

Below this line, the fetch logic itself is unchanged from before.
"""
import requests
import urllib.parse

API_URL = "https://kavitakosh.org/kk/api.php"
PAGE_URL = "https://kavitakosh.org/kk/index.php"
UA = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")}
POEM_CATEGORY = "श्रेणी:कविता"


def fetch_kavita_roj(max_tries=8):
    """Returns {"title": ..., "poet": ..., "url": ...} for one random poem,
    or None if no valid poem was found within max_tries (network failure,
    site down, or just bad luck) — caller should treat None as "skip the
    box today", same graceful-degradation pattern as everything else here."""
    for _ in range(max_tries):
        try:
            r = requests.get(API_URL, headers=UA, timeout=15, params={
                "action": "query", "list": "random", "rnnamespace": 0,
                "rnlimit": 1, "format": "json",
            })
            r.raise_for_status()
            candidates = r.json().get("query", {}).get("random", [])
            if not candidates:
                continue
            page = candidates[0]
            title, pageid = page.get("title", ""), page.get("id")

            # Poem pages are titled "<poem> / <poet>" (or, for translations,
            # "<poem> / <original poet> / <translator>" — rsplit on the LAST
            # " / " so the translator/credited author is what we show).
            if " / " not in title:
                continue

            # Confirm it's actually a cataloged poem, not some other page
            # that coincidentally has a slash in its title.
            r2 = requests.get(API_URL, headers=UA, timeout=15, params={
                "action": "query", "prop": "categories", "pageids": pageid,
                "clcategories": POEM_CATEGORY, "format": "json",
            })
            r2.raise_for_status()
            pages = r2.json().get("query", {}).get("pages", {})
            if not pages.get(str(pageid), {}).get("categories"):
                continue

            poem_title, poet_name = title.rsplit(" / ", 1)
            url = PAGE_URL + "?title=" + urllib.parse.quote(title.replace(" ", "_"), safe="")
            return {"title": poem_title.strip(), "poet": poet_name.strip(), "url": url}
        except Exception as e:
            print(f"[kavita] attempt failed: {e}")
            continue
    print(f"[kavita] WARNING: no valid poem found after {max_tries} tries — skipping today's box")
    return None


if __name__ == "__main__":
    result = fetch_kavita_roj()
    print(result)
