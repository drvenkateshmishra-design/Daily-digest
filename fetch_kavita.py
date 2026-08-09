"""Fetches a link to one random poem from Kavita Kosh (kavitakosh.org) for
the daily "Ek Kavita Roj" box.

IMPORTANT — this only ever returns a TITLE, a POET NAME, and a URL. It
never fetches or reproduces the poem's actual text. Kavita Kosh hosts both
centuries-old public-domain poets and living/recent copyrighted ones side
by side with no reliable automated way to tell them apart, so reproducing
full poem text daily would risk violating copyright regardless of which
poem happens to get picked. A link carries none of that risk — same reason
every news/blog story in this pipeline links out instead of scraping full
articles from sources that don't offer full text.

How it finds an actual poem (not a poet bio page, help page, etc.):
Kavita Kosh is a MediaWiki wiki. Individual poem pages are titled
"<poem title> / <poet name>" and are members of the category
"श्रेणी:कविता" (~71,000 pages as of Aug 2026). There's no "random member of
a category" API call available on this wiki (the RandomInCategory
extension isn't installed), so this asks the API for a random page from
the main namespace (list=random, which returns poem pages AND poet bio
pages AND anything else in that namespace, mixed) and retries until it
gets a title matching the "X / Y" poem format, then double-checks that
page is actually a member of श्रेणी:कविता before accepting it. In practice
poems vastly outnumber other main-namespace pages, so this usually
succeeds on the first or second try.
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
