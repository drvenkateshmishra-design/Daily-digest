"""Fetches recent journal articles from PubMed via NCBI E-utilities (free, no key needed)."""
import requests
import time
import xml.etree.ElementTree as ET
import config

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def _is_tier1(journal_name):
    name = (journal_name or "").lower()
    return any(t in name for t in config.TIER1_JOURNALS)


def _truncate(text, max_chars=None):
    max_chars = max_chars or getattr(config, "JOURNAL_ABSTRACT_MAX_CHARS", 600)
    text = " ".join(text.split())  # collapse whitespace
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0].rstrip(".,;: ") + "…"


def _fetch_abstracts(ids):
    """Returns dict: {pmid: abstract_text}. One request for all ids passed in —
    call this AFTER trimming to the articles you're actually keeping, not on
    every search hit, to stay polite to NCBI's rate limit."""
    if not ids:
        return {}
    try:
        r = requests.get(EFETCH, params={
            "db": "pubmed", "id": ",".join(ids),
            "rettype": "abstract", "retmode": "xml",
        }, timeout=25)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        abstracts = {}
        for article in root.findall(".//PubmedArticle"):
            pmid_el = article.find(".//PMID")
            if pmid_el is None or not pmid_el.text:
                continue
            pmid = pmid_el.text
            parts = []
            for ab in article.findall(".//Abstract/AbstractText"):
                label = ab.get("Label")
                text = "".join(ab.itertext()).strip()
                if not text:
                    continue
                parts.append(f"{label}: {text}" if label else text)
            if parts:
                abstracts[pmid] = _truncate(" ".join(parts))
        return abstracts
    except Exception as e:
        print(f"[journals] Error fetching abstracts for {len(ids)} article(s): {e}")
        return {}


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
        articles = articles[:config.MAX_ARTICLES_PER_SECTION]

        # Only fetch abstracts for the articles we're actually keeping.
        time.sleep(0.34)  # NCBI unauthenticated rate limit is 3 req/sec
        abstracts = _fetch_abstracts([a["pmid"] for a in articles])
        for a in articles:
            a["excerpt"] = abstracts.get(a["pmid"], "")  # same key as news items use, so
            # build_pdf.py's shared _story_block() renders it with zero changes needed there.

        return articles
    except Exception as e:
        print(f"[journals] Error fetching '{term[:40]}...': {e}")
        return []


def fetch_journals():
    """Returns dict: {section_name: [ {title, journal, pubdate, link, tier1, excerpt} ]}"""
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
            if it["excerpt"]:
                print(f"    {it['excerpt'][:150]}...")
