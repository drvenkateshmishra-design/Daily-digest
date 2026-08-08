# Add these entries to NEWS_FEEDS in config.py, alongside the existing
# "Health & Medicine" / "AI" / "India & General" sections.

NEW_NEWS_FEEDS_SECTIONS = {
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
    "Editorials & Opinion": [
        "https://www.thehindu.com/opinion/feeder/default.rss",
        "http://indianexpress.com/section/opinion/feed/",
        "https://www.hindustantimes.com/feeds/rss/opinion/rssfeed.xml",
        "https://www.thehindubusinessline.com/opinion/feeder/default.rss",
        # Hindi-language editorials
        "https://www.bhaskar.com/rss-feed/1061/",              # Dainik Bhaskar - देश (national desk incl. edit pieces)
        "https://www.jansatta.com/feed/",                       # Jansatta (IE's Hindi paper) - opinion-heavy
        "https://feed.livehindustan.com/rss/3127",              # Live Hindustan
    ],
}

# Note on reliability: feedparser fails silently per-feed (returns an empty
# entry list) rather than crashing, so a dead/renamed URL here just means
# that one source contributes nothing that day - it won't break the run.
# Worth spot-checking these once after the first live run and pruning any
# that come back empty for a few days running (paywalled editorial pages
# in particular sometimes truncate their RSS to nothing).
