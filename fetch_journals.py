"""Fetches recent journal articles from PubMed via NCBI E-utilities (free, no key needed)."""
import requests
import time

import config

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def _is_tier1(journal_name):
    name = (journal_name or "").lower()
    return any(t in name for t in config.TIER1_JOURNALS)


def _fetch_section(term):
    query = f'({term}) AND ("last {config.PUBMED_LOOKBACK_DAYS} days"[PDat])'
    try:
        r = requests.get(ESEARCH, params={
            "db": "pubmed", "term": query, "retmax": 40,
            "sort": "date", "retmode": "json",
        }, timeout=20)
        r.raise_for_status()
        ids = r.json()["esearchresult"]["idlist"]
        if not ids:
            return []

        r2 = requests.get(ESUMMARY, params={
            "db": "pubmed", "id": ",".join(ids), "retmode": "json",
        }, timeout=20)
        r2.raise_for_status()
        data = r2.json()["result"]

        articles = []
        for pmid in ids:
            item = data.get(pmid)
            if not item:
                continue
            journal = item.get("fulljournalname", "")
            articles.append({
                "pmid": pmid,
                "title": item.get("title", "Untitled").strip().rstrip("."),
                "journal": journal,
                "pubdate": item.get("pubdate", ""),
                "link": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "tier1": _is_tier1(journal),
            })

        # Tier-1 journals first, then by recency (list is already date-sorted from esearch)
        articles.sort(key=lambda a: not a["tier1"])
        return articles[:config.MAX_ARTICLES_PER_SECTION]

    except Exception as e:
        print(f"[journals] Error fetching '{term[:40]}...': {e}")
        return []


def fetch_journals():
    """Returns dict: {section_name: [ {title, journal, pubdate, link, tier1} ]}"""
    results = {}
    for section, term in config.JOURNAL_SEARCHES.items():
        results[section] = _fetch_section(term)
        time.sleep(0.5)  # be polite to NCBI's rate limit (3 req/sec unauthenticated)
    return results


if __name__ == "__main__":
    journals = fetch_journals()
    for section, items in journals.items():
        print(f"\n=== {section} ({len(items)}) ===")
        for it in items:
            star = "★" if it["tier1"] else " "
            print(f"{star} {it['title'][:70]}  [{it['journal']}]")
