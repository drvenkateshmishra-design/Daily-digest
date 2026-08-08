"""
Edit this file to change what shows up in your digest.
No need to touch any other file for day-to-day tweaks.
"""

# ---- NEWS: RSS feeds, grouped under a section heading ----
NEWS_FEEDS = {
    "Health & Medicine": [
        "https://www.statnews.com/feed/",
        "https://www.sciencedaily.com/rss/health_medicine.xml",
        "https://medicalxpress.com/rss-feed/",
    ],
    "AI": [
        "https://venturebeat.com/category/ai/feed/",
        "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    ],
    "India & General": [
        "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
        "https://feeds.feedburner.com/ndtvnews-india-news",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
    ],
    "Tech & Gadgets": [
        "https://gadgets360.com/rss/feeds",           # Gadgets360 - news
        "https://gadgets360.com/rss/reviews",         # Gadgets360 - reviews
        "https://www.gsmarena.com/rss-news-reviews.php3",
        "http://feeds.feedburner.com/techgenyz",
    ],
    "Bollywood & Entertainment": [
        "https://www.bollywoodhungama.com/feed",
        "https://www.pinkvilla.com/rss.xml",
        "https://www.filmfare.com/feeds/feeds.xml",
    ],
    "Sports": [
        "http://www.espncricinfo.com/rss/content/story/feeds/0.xml",
        "http://feeds.feedburner.com/ndtvsports-cricket",
        "https://www.sportskeeda.com/feed",
        "http://feeds.bbci.co.uk/sport/rss.xml",
    ],
}
MAX_NEWS_ITEMS_PER_SECTION = 6
NEWS_MAX_AGE_HOURS = 96  # only include items published in the last N hours (some feeds post infrequently)
NEWS_EXCERPT_MAX_CHARS = 500  # length of the excerpt shown under each headline — tune 300-800

# ---- JOURNALS: PubMed search terms per section ----
# These are PubMed search syntax. Edit the keywords, not the [Title/Abstract] tags.
JOURNAL_SEARCHES = {
    "Pediatrics": '(pediatric*[Title/Abstract] OR paediatric*[Title/Abstract])',
    "Pediatric Critical Care": '(PICU[Title/Abstract] OR "pediatric critical care"[Title/Abstract] OR "pediatric intensive care"[Title/Abstract])',
    "AI in Healthcare": '(("artificial intelligence"[Title/Abstract] OR "machine learning"[Title/Abstract] OR "large language model"[Title/Abstract]) AND (health*[Title/Abstract] OR clinical[Title/Abstract] OR medic*[Title/Abstract]))',
}
PUBMED_LOOKBACK_DAYS = 7
MAX_ARTICLES_PER_SECTION = 8

# Journals treated as "high priority" — these get sorted to the top of each section.
# Match is case-insensitive substring match against PubMed's journal name.
TIER1_JOURNALS = [
    "new england journal of medicine", "lancet", "jama", "nature medicine",
    "pediatrics", "jama pediatrics", "pediatric critical care medicine",
    "the lancet child & adolescent health", "critical care medicine",
    "intensive care medicine", "npj digital medicine", "nature",
]

# ---- DELIVERY ----
# Gmail App Password auth — GMAIL_ADDRESS, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL
# all come from GitHub Actions secrets — do not hardcode them here.

# ---- OUTPUT ----
PDF_TITLE = "Venki Times"
TIMEZONE = "Asia/Kolkata"
