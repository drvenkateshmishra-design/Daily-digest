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
        # NDTV's own feed reports a broken/garbled <channel><title> ("NDTV
        # News Search Records Found 1000") — this override tuple form
        # (url, display_name) forces the real name in the byline instead.
        # See fetch_news.py: any entry can be a plain url string, or a
        # (url, display_name) tuple to override a broken feed-reported name.
        ("https://feeds.feedburner.com/ndtvnews-india-news", "NDTV News"),
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.thebetterindia.com/feed/",  # verified full-text (median ~1.9K chars), fresh daily, solutions/human-interest journalism
        # ptinews.com requested too, but its whole site 403s (even the
        # homepage) regardless of User-Agent — no feed to add, not a code issue.
    ],
    "Tech & Gadgets": [
        # Gadgets360's two feeds 403 unconditionally (confirmed: still 403
        # even with a full browser User-Agent — infra-level IP block, not
        # a UA issue) — dropped, replaced with Android Police below.
        "https://www.gsmarena.com/rss-news-reviews.php3",
        "http://feeds.feedburner.com/techgenyz",
        "https://www.androidpolice.com/feed/",  # verified live, headline+excerpt (not full-text, fine for NEWS)
    ],
    "Bollywood & Entertainment": [
        "https://www.bollywoodhungama.com/feed",
        "https://www.pinkvilla.com/rss.xml",
        # Filmfare 403s unconditionally — dropped, replaced with BH's own
        # news-specific feed (verified: real article bodies, not teasers).
        "https://www.bollywoodhungama.com/rss/news.xml",
    ],
    "Sports": [
        "http://www.espncricinfo.com/rss/content/story/feeds/0.xml",
        "http://feeds.feedburner.com/ndtvsports-cricket",
        "http://feeds.bbci.co.uk/sport/rss.xml",
        # Sportskeeda 403s unconditionally — dropped, replaced with
        # Cricinfo's India-team-tagged feed (verified live today).
        "https://www.espncricinfo.com/rss/content/story/feeds/6.xml",
    ],
}
MAX_NEWS_ITEMS_PER_SECTION = 6
NEWS_MAX_AGE_HOURS = 96  # only include items published in the last N hours
NEWS_EXCERPT_MAX_CHARS = 500  # length of the excerpt shown under each headline

# ---- BLOGS: long-form sources — these feeds carry full post text, not just a teaser ----
BLOG_FEEDS = {
    "Pediatrics & Medicine": [
        "https://dontforgetthebubbles.com/feed/",
        "https://pedemmorsels.com/feed/",
        "https://rebelem.com/medical-category/pediatrics/feed/",
        # Needs a browser User-Agent to avoid a 403 (now sent by default in
        # fetch_news.py) — verified real content, but medium-length (~450
        # chars, more substantial excerpt than true full-text posts).
        "https://www.kevinmd.com/feed",
    ],
    "AI, ML & Data Science": [
        "https://www.interconnects.ai/feed",
        "https://magazine.sebastianraschka.com/feed",
        "https://thegradient.pub/rss/",
        "https://www.latent.space/feed",
        "https://simonwillison.net/atom/everything/",  # verified full-text, near-daily
        "https://jack-clark.net/feed/",  # Import AI — verified full-text, long-form
    ],
    "Indian Commentary": [
        "https://publicpolicy.substack.com/feed",
        "https://ajayshahblog.blogspot.com/feeds/posts/default",
        "https://takshashiladispatch.substack.com/feed",
        "https://feeds.feedburner.com/indiauncut-full",
        "https://swarajyamag.com/feed",  # verified full-text (NOT /commentary/feed, which 404s)
    ],
    "Science & Technology": [
        "https://www.construction-physics.com/feed",
        "https://www.asimov.press/feed",
        # Quanta Magazine's RSS (incl. the api.quantamagazine.org endpoint)
        # was tested and only returns ~400-char teasers, not full text —
        # deliberately not added despite its reputation.
    ],
    "Space": [
        "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "https://briankoberlein.com/index.xml",
        "https://behindtheblack.com/feed/",  # verified real full posts (Robert Zimmerman), near-daily
    ],
    "Astrophotography": [
        "https://astroblogger.blogspot.com/feeds/posts/default",
        "https://astrobackyard.com/feed/",
    ],
    "Photography": [
        "https://blog.mingthein.com/feed/",
    ],
    "Physics": [
        "https://www.math.columbia.edu/~woit/wordpress/?feed=rss2",
        "https://www.preposterousuniverse.com/blog/feed/",
        # profmattstrassler.com/feed and backreaction.blogspot.com were
        # tested — the former's feed has only 1 entry, dated 6 months ago
        # (dormant), the latter is teaser-only despite its reputation.
        # Neither cleared the bar, so neither was added.
    ],
    "Minimalism": [
        "https://nourishingminimalism.com/feed",  # verified: excellent full-text, near-daily
        "https://www.theminimalists.com/feed/",  # verified: full-text, mixed length but substantial
        "https://leibal.com/feed/",  # verified: full-text, design/product-focused minimalism
        # zenhabits.net/feed (404, dead), becomingminimalist (feed serves
        # stale cached content dated 2008), simplelionheartlife (returns
        # HTTP 202 with no entries, unusable) were all tested and rejected.
    ],
    "Spirituality": [
        "https://dhammafootsteps.com/feed/",  # verified full-text (Theravada/Advaita) — posts infrequently, latest ~2 months old as of this writing
        "https://feeds.feedburner.com/theexistentialbuddhist",  # verified full-text, ~2-3 week cadence
        # wildmind.org (both feed paths return HTTP 202 with no entries,
        # unusable), sameoldzen (mostly empty-body entries), edcyzewski.com
        # (full-text but dormant ~4.5 months), mindfulbalance.org (fresh but
        # teaser-only) were all tested and rejected. This section is
        # thinner than the others as a result — say the word if you want
        # another pass at finding more.
    ],
    "Movies & TV": [
        "https://www.rogerebert.com/feed",  # verified excellent full-text reviews (median ~9K chars), covers film + streaming TV, daily
        "https://screenhub.blog/feed",  # verified full-text (median ~5.7K chars), film essays/retrospectives
        # indiewire.com, thefilmexperience.net, decentfilms.com were tested
        # and rejected (teaser-only, 503, or 404 respectively).
    ],
    "Indian Movies & Web Series": [
        "https://koimoi.com/category/reviews/feed/",  # verified excellent full-text (median ~4.3K chars), fresh daily — covers both theatrical & OTT/web-series reviews
        "https://www.bollywoodhungama.com/rss/movie-review.xml",  # verified excellent full-text (median ~4.7K chars), fresh, dedicated review feed
        # filmcompanion.in (0 entries — feed currently broken despite the
        # site's reputation), dontcallitbollywood.com (full-text but
        # dormant ~7 months), ottplay.com (403) were tested and rejected.
    ],
    "Books": [
        "https://www.theparisreview.org/blog/feed/",  # verified excellent full-text (median ~12.7K chars), literary essays/reviews
        "https://bookriot.com/feed/",  # verified real content (median ~700 chars — shorter, more like a strong excerpt than full-text, but genuine)
        "https://feeds.feedburner.com/BigalsBooksAndPals",  # verified full-text (median ~2.9K chars), indie/self-pub book reviews
        # alittleblogofbooks.com (teaser-only) and washingtonindependentreviewofbooks.com (404) were tested and rejected.
    ],
}
BLOG_MAX_AGE_HOURS = 168  # 1 week — blogs post less often than news
MAX_BLOG_ITEMS_PER_SECTION = 3
BLOG_EXCERPT_MAX_CHARS = 3000  # long-form — the whole point is full text, not a teaser

# ---- JOURNALS: PubMed search terms per section ----
# These are PubMed search syntax. Edit the keywords, not the [Title/Abstract] tags.
JOURNAL_SEARCHES = {
    "Pediatrics": '(pediatric*[Title/Abstract] OR paediatric*[Title/Abstract])',
    "Pediatric Critical Care": '(PICU[Title/Abstract] OR "pediatric critical care"[Title/Abstract] OR "pediatric intensive care"[Title/Abstract])',
    "AI in Healthcare": '(("artificial intelligence"[Title/Abstract] OR "machine learning"[Title/Abstract] OR "large language model"[Title/Abstract]) AND (health*[Title/Abstract] OR clinical[Title/Abstract] OR medic*[Title/Abstract]))',
}
PUBMED_LOOKBACK_DAYS = 7
MAX_ARTICLES_PER_SECTION = 8
JOURNAL_ABSTRACT_MAX_CHARS = 600

# Journals treated as "high priority" — sorted to the top of each section.
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

# ---- FRONT-PAGE "THOUGHTS FOR THE DAY" ----
# All entries below are centuries-old, unambiguously public-domain classical
# material (Upanishads/Gita/Hitopadesha/Chanakya Niti/Manusmriti, and
# Kabir/Rahim/Tulsidas dohas, all pre-1700s) — safe to reproduce in full,
# unlike modern copyrighted poetry. One of each is picked per day (seeded by
# date, so a same-day rerun shows the same picks rather than shuffling).

SANSKRIT_QUOTES = [
    {"deva": "सत्यमेव जयते", "translit": "satyameva jayate",
     "meaning": "Truth alone triumphs", "source": "Mundaka Upanishad"},
    {"deva": "वसुधैव कुटुम्बकम्", "translit": "vasudhaiva kutumbakam",
     "meaning": "The whole world is one family", "source": "Maha Upanishad"},
    {"deva": "अहिंसा परमो धर्मः", "translit": "ahimsa paramo dharmah",
     "meaning": "Non-violence is the supreme duty", "source": "Mahabharata"},
    {"deva": "विद्या ददाति विनयम्", "translit": "vidya dadati vinayam",
     "meaning": "Knowledge gives humility", "source": "Hitopadesha"},
    {"deva": "योगः कर्मसु कौशलम्", "translit": "yogah karmasu kaushalam",
     "meaning": "Skill in action is yoga", "source": "Bhagavad Gita 2.50"},
    {"deva": "सर्वे भवन्तु सुखिनः", "translit": "sarve bhavantu sukhinah",
     "meaning": "May all beings be happy", "source": "Shanti Mantra"},
    {"deva": "उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः", "translit": "udyamena hi sidhyanti karyani na manorathaih",
     "meaning": "Deeds succeed through effort, not mere wishing", "source": "Hitopadesha"},
    {"deva": "न हि ज्ञानेन सदृशं पवित्रमिह विद्यते", "translit": "na hi gyanena sadrisham pavitramiha vidyate",
     "meaning": "Nothing in this world purifies like knowledge", "source": "Bhagavad Gita 4.38"},
    {"deva": "आत्मनः प्रतिकूलानि परेषां न समाचरेत्", "translit": "atmanah pratikulani pareshaam na samacharet",
     "meaning": "Do not do to others what is disagreeable to yourself", "source": "Mahabharata"},
    {"deva": "क्षणशः कणशश्चैव विद्यामर्थं च साधयेत्", "translit": "kshanashah kanashashchaiva vidyamartham cha sadhayet",
     "meaning": "Acquire knowledge and wealth bit by bit, moment by moment", "source": "Chanakya Niti"},
    {"deva": "धर्मो रक्षति रक्षितः", "translit": "dharmo rakshati rakshitah",
     "meaning": "Dharma protects those who protect it", "source": "Manusmriti"},
    {"deva": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन", "translit": "karmanyevadhikaraste ma phaleshu kadachana",
     "meaning": "Your right is to action alone, never to its fruits", "source": "Bhagavad Gita 2.47"},
    {"deva": "शरीरमाद्यं खलु धर्मसाधनम्", "translit": "shariramadyam khalu dharma-sadhanam",
     "meaning": "The body is indeed the foremost instrument of dharma", "source": "Kalidasa, Kumarasambhava"},
    {"deva": "परोपकारः पुण्याय पापाय परपीडनम्", "translit": "paropakarah punyaya papaya parapidanam",
     "meaning": "Helping others is virtue; hurting others is sin", "source": "attributed to Vyasa"},
]

ENGLISH_QUOTES = [
    {"text": "The unexamined life is not worth living.", "author": "Socrates"},
    {"text": "He who has a why to live can bear almost any how.", "author": "Friedrich Nietzsche"},
    {"text": "It is not that we have a short time to live, but that we waste a lot of it.", "author": "Seneca"},
    {"text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein"},
    {"text": "Do not go where the path may lead, go instead where there is no path and leave a trail.", "author": "Ralph Waldo Emerson"},
    {"text": "The best time to plant a tree was 20 years ago. The second best time is now.", "author": "Chinese Proverb"},
    {"text": "Knowing yourself is the beginning of all wisdom.", "author": "Aristotle"},
    {"text": "Whatever you are, be a good one.", "author": "Abraham Lincoln"},
    {"text": "The only true wisdom is in knowing you know nothing.", "author": "Socrates"},
    {"text": "We must be the change we wish to see in the world.", "author": "Mahatma Gandhi"},
    {"text": "Well done is better than well said.", "author": "Benjamin Franklin"},
    {"text": "Character is destiny.", "author": "Heraclitus"},
    {"text": "Nothing in life is to be feared, it is only to be understood.", "author": "Marie Curie"},
    {"text": "The mind is everything. What you think you become.", "author": "attributed to the Buddha"},
]

# Classical dohas only (Kabir, Rahim, Tulsidas — all pre-1700s, public domain).
# Deliberately NOT sourced from Kavita Kosh or similar live archives, which mix
# in 20th/21st-century poets whose work is still under copyright — see chat.
HINDI_POEMS = [
    {"lines": "बुरा जो देखन मैं चला, बुरा न मिलिया कोय।<br/>जो मन खोजा आपना, मुझसे बुरा न कोय॥", "poet": "कबीर (Kabir)"},
    {"lines": "माटी कहे कुम्हार से, तू क्या रौंदे मोहि।<br/>एक दिन ऐसा आयेगा, मैं रौंदूंगी तोहि॥", "poet": "कबीर (Kabir)"},
    {"lines": "साईं इतना दीजिए, जा में कुटुम्ब समाय।<br/>मैं भी भूखा न रहूँ, साधु न भूखा जाय॥", "poet": "कबीर (Kabir)"},
    {"lines": "जब मैं था तब हरि नहीं, अब हरि हैं मैं नाहिं।<br/>सब अँधियारा मिट गया, जब दीपक देख्या माहिं॥", "poet": "कबीर (Kabir)"},
    {"lines": "पोथी पढ़ि पढ़ि जग मुआ, पंडित भया न कोय।<br/>ढाई आखर प्रेम का, पढ़े सो पंडित होय॥", "poet": "कबीर (Kabir)"},
    {"lines": "कस्तूरी कुंडल बसे, मृग ढूँढे बन माहि।<br/>ऐसे घट घट राम है, दुनिया देखे नाहि॥", "poet": "कबीर (Kabir)"},
    {"lines": "दुख में सुमिरन सब करे, सुख में करे न कोय।<br/>जो सुख में सुमिरन करे, तो दुख काहे को होय॥", "poet": "कबीर (Kabir)"},
    {"lines": "रहिमन धागा प्रेम का, मत तोड़ो चटकाय।<br/>टूटे से फिर ना जुड़े, जुड़े गाँठ पड़ जाय॥", "poet": "रहीम (Rahim)"},
    {"lines": "बड़े बड़ाई ना करें, बड़े न बोलें बोल।<br/>रहिमन हीरा कब कहे, लाख टका मेरो मोल॥", "poet": "रहीम (Rahim)"},
    {"lines": "रहिमन पानी राखिए, बिन पानी सब सून।<br/>पानी गए न ऊबरे, मोती मानुष चून॥", "poet": "रहीम (Rahim)"},
    {"lines": "परहित सरिस धर्म नहिं भाई।<br/>पर पीड़ा सम नहिं अधमाई॥", "poet": "तुलसीदास (Tulsidas)"},
    {"lines": "तुलसी साथी विपत्ति के, विद्या, विनय, विवेक।<br/>साहस, सुकृत, सुसत्यव्रत, राम भरोसे एक॥", "poet": "तुलसीदास (Tulsidas)"},
]


# ---- EK KAVITA ROJ (daily poem link) ----
# One entry picked per day (date-seeded, same pattern as the quotes above).
# Unlike the quotes above, this is title + poet + LINK ONLY — never the poem
# text itself. Kavita Kosh mixes public-domain and living/copyrighted poets
# with no reliable way to auto-filter, so a link (not reproduction) is what
# makes this safe regardless of which poem gets picked.
#
# This is a pre-verified STATIC pool, not a live daily fetch — GitHub
# Actions runner IPs get a blanket 403 from kavitakosh.org (confirmed: the
# exact same request that works fine from other environments fails 8/8
# times from GH Actions, and unrelated Substack feeds hit the same 403
# from the same runner — this is IP-range blocking on their end, not
# anything wrong with the request). A live per-day API call would just
# fail every single day it runs in Actions, so this pool was generated
# once (Aug 2026) from an environment that isn't blocked, each entry
# individually verified as a real category-tagged poem page. To regenerate
# or grow this pool later (e.g. from a machine/network that isn't
# IP-blocked), see fetch_kavita.py — it now exists as a standalone utility
# script for that, no longer imported by main.py.
KAVITA_ROJ_POEMS = [
    {"title": "तुझसे तो कोई गिला नहीं है", "poet": "परवीन शाकिर", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A4%E0%A5%81%E0%A4%9D%E0%A4%B8%E0%A5%87_%E0%A4%A4%E0%A5%8B_%E0%A4%95%E0%A5%8B%E0%A4%88_%E0%A4%97%E0%A4%BF%E0%A4%B2%E0%A4%BE_%E0%A4%A8%E0%A4%B9%E0%A5%80%E0%A4%82_%E0%A4%B9%E0%A5%88_%2F_%E0%A4%AA%E0%A4%B0%E0%A4%B5%E0%A5%80%E0%A4%A8_%E0%A4%B6%E0%A4%BE%E0%A4%95%E0%A4%BF%E0%A4%B0"},
    {"title": "कुखुरो", "poet": "लक्ष्मीप्रसाद देवकोटा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A5%81%E0%A4%96%E0%A5%81%E0%A4%B0%E0%A5%8B_%2F_%E0%A4%B2%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A5%8D%E0%A4%AE%E0%A5%80%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B8%E0%A4%BE%E0%A4%A6_%E0%A4%A6%E0%A5%87%E0%A4%B5%E0%A4%95%E0%A5%8B%E0%A4%9F%E0%A4%BE"},
    {"title": "अनंत", "poet": "सुदर्शन प्रियदर्शिनी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%85%E0%A4%A8%E0%A4%82%E0%A4%A4_%2F_%E0%A4%B8%E0%A5%81%E0%A4%A6%E0%A4%B0%E0%A5%8D%E0%A4%B6%E0%A4%A8_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF%E0%A4%A6%E0%A4%B0%E0%A5%8D%E0%A4%B6%E0%A4%BF%E0%A4%A8%E0%A5%80"},
    {"title": "श्री गुरु-गोपाल वन्दना", "poet": "यमुना प्रसाद चतुर्वेदी 'प्रीतम'", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80_%E0%A4%97%E0%A5%81%E0%A4%B0%E0%A5%81-%E0%A4%97%E0%A5%8B%E0%A4%AA%E0%A4%BE%E0%A4%B2_%E0%A4%B5%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A4%A8%E0%A4%BE_%2F_%E0%A4%AF%E0%A4%AE%E0%A5%81%E0%A4%A8%E0%A4%BE_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B8%E0%A4%BE%E0%A4%A6_%E0%A4%9A%E0%A4%A4%E0%A5%81%E0%A4%B0%E0%A5%8D%E0%A4%B5%E0%A5%87%E0%A4%A6%E0%A5%80_%27%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%A4%E0%A4%AE%27"},
    {"title": "फ़र्क पड़ता है", "poet": "प्रियंका गुप्ता", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AB%E0%A4%BC%E0%A4%B0%E0%A5%8D%E0%A4%95_%E0%A4%AA%E0%A4%A1%E0%A4%BC%E0%A4%A4%E0%A4%BE_%E0%A4%B9%E0%A5%88_%2F_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF%E0%A4%82%E0%A4%95%E0%A4%BE_%E0%A4%97%E0%A5%81%E0%A4%AA%E0%A5%8D%E0%A4%A4%E0%A4%BE"},
    {"title": "बाटोखनी जाने सहिदहरू", "poet": "कृष्णभूषण बल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A4%BE%E0%A4%9F%E0%A5%8B%E0%A4%96%E0%A4%A8%E0%A5%80_%E0%A4%9C%E0%A4%BE%E0%A4%A8%E0%A5%87_%E0%A4%B8%E0%A4%B9%E0%A4%BF%E0%A4%A6%E0%A4%B9%E0%A4%B0%E0%A5%82_%2F_%E0%A4%95%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A3%E0%A4%AD%E0%A5%82%E0%A4%B7%E0%A4%A3_%E0%A4%AC%E0%A4%B2"},
    {"title": "आत्मघाती आत्मा", "poet": "विपिन चौधरी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%86%E0%A4%A4%E0%A5%8D%E0%A4%AE%E0%A4%98%E0%A4%BE%E0%A4%A4%E0%A5%80_%E0%A4%86%E0%A4%A4%E0%A5%8D%E0%A4%AE%E0%A4%BE_%2F_%E0%A4%B5%E0%A4%BF%E0%A4%AA%E0%A4%BF%E0%A4%A8_%E0%A4%9A%E0%A5%8C%E0%A4%A7%E0%A4%B0%E0%A5%80"},
    {"title": "पेड़ से", "poet": "केदारनाथ अग्रवाल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AA%E0%A5%87%E0%A4%A1%E0%A4%BC_%E0%A4%B8%E0%A5%87_%2F_%E0%A4%95%E0%A5%87%E0%A4%A6%E0%A4%BE%E0%A4%B0%E0%A4%A8%E0%A4%BE%E0%A4%A5_%E0%A4%85%E0%A4%97%E0%A5%8D%E0%A4%B0%E0%A4%B5%E0%A4%BE%E0%A4%B2"},
    {"title": "चाल भतूळा रेत रमां! : अेक", "poet": "राजूराम बिजारणियां", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9A%E0%A4%BE%E0%A4%B2_%E0%A4%AD%E0%A4%A4%E0%A5%82%E0%A4%B3%E0%A4%BE_%E0%A4%B0%E0%A5%87%E0%A4%A4_%E0%A4%B0%E0%A4%AE%E0%A4%BE%E0%A4%82%21_%3A_%E0%A4%85%E0%A5%87%E0%A4%95_%2F_%E0%A4%B0%E0%A4%BE%E0%A4%9C%E0%A5%82%E0%A4%B0%E0%A4%BE%E0%A4%AE_%E0%A4%AC%E0%A4%BF%E0%A4%9C%E0%A4%BE%E0%A4%B0%E0%A4%A3%E0%A4%BF%E0%A4%AF%E0%A4%BE%E0%A4%82"},
    {"title": "किस लोक में", "poet": "नीलेश रघुवंशी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A4%BF%E0%A4%B8_%E0%A4%B2%E0%A5%8B%E0%A4%95_%E0%A4%AE%E0%A5%87%E0%A4%82_%2F_%E0%A4%A8%E0%A5%80%E0%A4%B2%E0%A5%87%E0%A4%B6_%E0%A4%B0%E0%A4%98%E0%A5%81%E0%A4%B5%E0%A4%82%E0%A4%B6%E0%A5%80"},
    {"title": "रीझ-रिझावण", "poet": "भंवर कसाना", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B0%E0%A5%80%E0%A4%9D-%E0%A4%B0%E0%A4%BF%E0%A4%9D%E0%A4%BE%E0%A4%B5%E0%A4%A3_%2F_%E0%A4%AD%E0%A4%82%E0%A4%B5%E0%A4%B0_%E0%A4%95%E0%A4%B8%E0%A4%BE%E0%A4%A8%E0%A4%BE"},
    {"title": "पांव भर बैठने की जमीन", "poet": "लक्ष्मीकान्त मुकुल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AA%E0%A4%BE%E0%A4%82%E0%A4%B5_%E0%A4%AD%E0%A4%B0_%E0%A4%AC%E0%A5%88%E0%A4%A0%E0%A4%A8%E0%A5%87_%E0%A4%95%E0%A5%80_%E0%A4%9C%E0%A4%AE%E0%A5%80%E0%A4%A8_%2F_%E0%A4%B2%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A5%8D%E0%A4%AE%E0%A5%80%E0%A4%95%E0%A4%BE%E0%A4%A8%E0%A5%8D%E0%A4%A4_%E0%A4%AE%E0%A5%81%E0%A4%95%E0%A5%81%E0%A4%B2"},
    {"title": "जिस देश में गंगा बहती है", "poet": "विमल राजस्थानी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9C%E0%A4%BF%E0%A4%B8_%E0%A4%A6%E0%A5%87%E0%A4%B6_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%97%E0%A4%82%E0%A4%97%E0%A4%BE_%E0%A4%AC%E0%A4%B9%E0%A4%A4%E0%A5%80_%E0%A4%B9%E0%A5%88_%2F_%E0%A4%B5%E0%A4%BF%E0%A4%AE%E0%A4%B2_%E0%A4%B0%E0%A4%BE%E0%A4%9C%E0%A4%B8%E0%A5%8D%E0%A4%A5%E0%A4%BE%E0%A4%A8%E0%A5%80"},
    {"title": "समाधान", "poet": "ओकिउयामा ग्वाइन", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B8%E0%A4%AE%E0%A4%BE%E0%A4%A7%E0%A4%BE%E0%A4%A8_%2F_%E0%A4%93%E0%A4%95%E0%A4%BF%E0%A4%89%E0%A4%AF%E0%A4%BE%E0%A4%AE%E0%A4%BE_%E0%A4%97%E0%A5%8D%E0%A4%B5%E0%A4%BE%E0%A4%87%E0%A4%A8"},
    {"title": "जटिल बना तो बना मनुष्य", "poet": "मनोज कुमार झा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9C%E0%A4%9F%E0%A4%BF%E0%A4%B2_%E0%A4%AC%E0%A4%A8%E0%A4%BE_%E0%A4%A4%E0%A5%8B_%E0%A4%AC%E0%A4%A8%E0%A4%BE_%E0%A4%AE%E0%A4%A8%E0%A5%81%E0%A4%B7%E0%A5%8D%E0%A4%AF_%2F_%E0%A4%AE%E0%A4%A8%E0%A5%8B%E0%A4%9C_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0_%E0%A4%9D%E0%A4%BE"},
    {"title": "वज़ह-बेवज़ह", "poet": "बसंत त्रिपाठी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B5%E0%A4%9C%E0%A4%BC%E0%A4%B9-%E0%A4%AC%E0%A5%87%E0%A4%B5%E0%A4%9C%E0%A4%BC%E0%A4%B9_%2F_%E0%A4%AC%E0%A4%B8%E0%A4%82%E0%A4%A4_%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AA%E0%A4%BE%E0%A4%A0%E0%A5%80"},
    {"title": "बाँध दिए क्यों प्राण", "poet": "सुमित्रानंदन पंत", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A4%BE%E0%A4%81%E0%A4%A7_%E0%A4%A6%E0%A4%BF%E0%A4%8F_%E0%A4%95%E0%A5%8D%E0%A4%AF%E0%A5%8B%E0%A4%82_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A3_%2F_%E0%A4%B8%E0%A5%81%E0%A4%AE%E0%A4%BF%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A8%E0%A4%82%E0%A4%A6%E0%A4%A8_%E0%A4%AA%E0%A4%82%E0%A4%A4"},
    {"title": "लोहा बजेगा", "poet": "शील", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B2%E0%A5%8B%E0%A4%B9%E0%A4%BE_%E0%A4%AC%E0%A4%9C%E0%A5%87%E0%A4%97%E0%A4%BE_%2F_%E0%A4%B6%E0%A5%80%E0%A4%B2"},
    {"title": "क्रागुएवात्स में पूरे स्कूल के साथ तीसरी क्लास की परीक्षा", "poet": "सोमदत्त", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%97%E0%A5%81%E0%A4%8F%E0%A4%B5%E0%A4%BE%E0%A4%A4%E0%A5%8D%E0%A4%B8_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%AA%E0%A5%82%E0%A4%B0%E0%A5%87_%E0%A4%B8%E0%A5%8D%E0%A4%95%E0%A5%82%E0%A4%B2_%E0%A4%95%E0%A5%87_%E0%A4%B8%E0%A4%BE%E0%A4%A5_%E0%A4%A4%E0%A5%80%E0%A4%B8%E0%A4%B0%E0%A5%80_%E0%A4%95%E0%A5%8D%E0%A4%B2%E0%A4%BE%E0%A4%B8_%E0%A4%95%E0%A5%80_%E0%A4%AA%E0%A4%B0%E0%A5%80%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A4%BE_%2F_%E0%A4%B8%E0%A5%8B%E0%A4%AE%E0%A4%A6%E0%A4%A4%E0%A5%8D%E0%A4%A4"},
    {"title": "होटल ख़ुरासान", "poet": "असद ज़ैदी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B9%E0%A5%8B%E0%A4%9F%E0%A4%B2_%E0%A4%96%E0%A4%BC%E0%A5%81%E0%A4%B0%E0%A4%BE%E0%A4%B8%E0%A4%BE%E0%A4%A8_%2F_%E0%A4%85%E0%A4%B8%E0%A4%A6_%E0%A4%9C%E0%A4%BC%E0%A5%88%E0%A4%A6%E0%A5%80"},
    {"title": "दोसरोॅ सच-1", "poet": "चन्द्रप्रकाश जगप्रिय", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A6%E0%A5%8B%E0%A4%B8%E0%A4%B0%E0%A5%8B%E0%A5%85_%E0%A4%B8%E0%A4%9A-1_%2F_%E0%A4%9A%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%8D%E0%A4%B0%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%95%E0%A4%BE%E0%A4%B6_%E0%A4%9C%E0%A4%97%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF"},
    {"title": "वह", "poet": "विश्वनाथप्रसाद तिवारी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B5%E0%A4%B9_%2F_%E0%A4%B5%E0%A4%BF%E0%A4%B6%E0%A5%8D%E0%A4%B5%E0%A4%A8%E0%A4%BE%E0%A4%A5%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B8%E0%A4%BE%E0%A4%A6_%E0%A4%A4%E0%A4%BF%E0%A4%B5%E0%A4%BE%E0%A4%B0%E0%A5%80"},
    {"title": "हृदय-दीप में", "poet": "द्वारिका प्रसाद माहेश्वरी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B9%E0%A5%83%E0%A4%A6%E0%A4%AF-%E0%A4%A6%E0%A5%80%E0%A4%AA_%E0%A4%AE%E0%A5%87%E0%A4%82_%2F_%E0%A4%A6%E0%A5%8D%E0%A4%B5%E0%A4%BE%E0%A4%B0%E0%A4%BF%E0%A4%95%E0%A4%BE_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B8%E0%A4%BE%E0%A4%A6_%E0%A4%AE%E0%A4%BE%E0%A4%B9%E0%A5%87%E0%A4%B6%E0%A5%8D%E0%A4%B5%E0%A4%B0%E0%A5%80"},
    {"title": "प्रतिबिम्ब", "poet": "सुधा एम. राई", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%A4%E0%A4%BF%E0%A4%AC%E0%A4%BF%E0%A4%AE%E0%A5%8D%E0%A4%AC_%2F_%E0%A4%B8%E0%A5%81%E0%A4%A7%E0%A4%BE_%E0%A4%8F%E0%A4%AE._%E0%A4%B0%E0%A4%BE%E0%A4%88"},
    {"title": "कवि का जीवन", "poet": "अग्निशेखर", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A4%B5%E0%A4%BF_%E0%A4%95%E0%A4%BE_%E0%A4%9C%E0%A5%80%E0%A4%B5%E0%A4%A8_%2F_%E0%A4%85%E0%A4%97%E0%A5%8D%E0%A4%A8%E0%A4%BF%E0%A4%B6%E0%A5%87%E0%A4%96%E0%A4%B0"},
    {"title": "कंहिं सां न रीस काई न कोई रक़ीब आ", "poet": "अर्जुन ‘शाद’", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A4%82%E0%A4%B9%E0%A4%BF%E0%A4%82_%E0%A4%B8%E0%A4%BE%E0%A4%82_%E0%A4%A8_%E0%A4%B0%E0%A5%80%E0%A4%B8_%E0%A4%95%E0%A4%BE%E0%A4%88_%E0%A4%A8_%E0%A4%95%E0%A5%8B%E0%A4%88_%E0%A4%B0%E0%A4%95%E0%A4%BC%E0%A5%80%E0%A4%AC_%E0%A4%86_%2F_%E0%A4%85%E0%A4%B0%E0%A5%8D%E0%A4%9C%E0%A5%81%E0%A4%A8_%E2%80%98%E0%A4%B6%E0%A4%BE%E0%A4%A6%E2%80%99"},
    {"title": "आश्रय", "poet": "जया जादवानी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%86%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A4%AF_%2F_%E0%A4%9C%E0%A4%AF%E0%A4%BE_%E0%A4%9C%E0%A4%BE%E0%A4%A6%E0%A4%B5%E0%A4%BE%E0%A4%A8%E0%A5%80"},
    {"title": "बेटी सी माँ", "poet": "अरुणिमा अरुण कमल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A5%87%E0%A4%9F%E0%A5%80_%E0%A4%B8%E0%A5%80_%E0%A4%AE%E0%A4%BE%E0%A4%81_%2F_%E0%A4%85%E0%A4%B0%E0%A5%81%E0%A4%A3%E0%A4%BF%E0%A4%AE%E0%A4%BE_%E0%A4%85%E0%A4%B0%E0%A5%81%E0%A4%A3_%E0%A4%95%E0%A4%AE%E0%A4%B2"},
    {"title": "भूख की मार", "poet": "रामकृपाल गुप्ता", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AD%E0%A5%82%E0%A4%96_%E0%A4%95%E0%A5%80_%E0%A4%AE%E0%A4%BE%E0%A4%B0_%2F_%E0%A4%B0%E0%A4%BE%E0%A4%AE%E0%A4%95%E0%A5%83%E0%A4%AA%E0%A4%BE%E0%A4%B2_%E0%A4%97%E0%A5%81%E0%A4%AA%E0%A5%8D%E0%A4%A4%E0%A4%BE"},
    {"title": "काग़ज़ का हलफ़नामा", "poet": "कुमार कृष्ण", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A4%BE%E0%A4%97%E0%A4%BC%E0%A4%9C%E0%A4%BC_%E0%A4%95%E0%A4%BE_%E0%A4%B9%E0%A4%B2%E0%A4%AB%E0%A4%BC%E0%A4%A8%E0%A4%BE%E0%A4%AE%E0%A4%BE_%2F_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0_%E0%A4%95%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A3"},
    {"title": "सिर्फ़ तुम्हारे लिए", "poet": "एम० के० मधु", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B8%E0%A4%BF%E0%A4%B0%E0%A5%8D%E0%A4%AB%E0%A4%BC_%E0%A4%A4%E0%A5%81%E0%A4%AE%E0%A5%8D%E0%A4%B9%E0%A4%BE%E0%A4%B0%E0%A5%87_%E0%A4%B2%E0%A4%BF%E0%A4%8F_%2F_%E0%A4%8F%E0%A4%AE%E0%A5%A6_%E0%A4%95%E0%A5%87%E0%A5%A6_%E0%A4%AE%E0%A4%A7%E0%A5%81"},
    {"title": "आफू खाय भांग मसकावे", "poet": "गोरखनाथ", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%86%E0%A4%AB%E0%A5%82_%E0%A4%96%E0%A4%BE%E0%A4%AF_%E0%A4%AD%E0%A4%BE%E0%A4%82%E0%A4%97_%E0%A4%AE%E0%A4%B8%E0%A4%95%E0%A4%BE%E0%A4%B5%E0%A5%87_%2F_%E0%A4%97%E0%A5%8B%E0%A4%B0%E0%A4%96%E0%A4%A8%E0%A4%BE%E0%A4%A5"},
    {"title": "बनते-बिगड़ते", "poet": "ज्योतिकृष्ण वर्मा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A4%A8%E0%A4%A4%E0%A5%87-%E0%A4%AC%E0%A4%BF%E0%A4%97%E0%A4%A1%E0%A4%BC%E0%A4%A4%E0%A5%87_%2F_%E0%A4%9C%E0%A5%8D%E0%A4%AF%E0%A5%8B%E0%A4%A4%E0%A4%BF%E0%A4%95%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A3_%E0%A4%B5%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE"},
    {"title": "प्रिये", "poet": "सीमा 'असीम' सक्सेना", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF%E0%A5%87_%2F_%E0%A4%B8%E0%A5%80%E0%A4%AE%E0%A4%BE_%27%E0%A4%85%E0%A4%B8%E0%A5%80%E0%A4%AE%27_%E0%A4%B8%E0%A4%95%E0%A5%8D%E0%A4%B8%E0%A5%87%E0%A4%A8%E0%A4%BE"},
    {"title": "भिक्षु", "poet": "अवतार एनगिल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AD%E0%A4%BF%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A5%81_%2F_%E0%A4%85%E0%A4%B5%E0%A4%A4%E0%A4%BE%E0%A4%B0_%E0%A4%8F%E0%A4%A8%E0%A4%97%E0%A4%BF%E0%A4%B2"},
    {"title": "एक युवा अधिकारी", "poet": "कृष्ण कुमार यादव", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%8F%E0%A4%95_%E0%A4%AF%E0%A5%81%E0%A4%B5%E0%A4%BE_%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%80_%2F_%E0%A4%95%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A3_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0_%E0%A4%AF%E0%A4%BE%E0%A4%A6%E0%A4%B5"},
    {"title": "मेसोपोटामिया के घेट्टो", "poet": "अनिल अनलहातु", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A5%87%E0%A4%B8%E0%A5%8B%E0%A4%AA%E0%A5%8B%E0%A4%9F%E0%A4%BE%E0%A4%AE%E0%A4%BF%E0%A4%AF%E0%A4%BE_%E0%A4%95%E0%A5%87_%E0%A4%98%E0%A5%87%E0%A4%9F%E0%A5%8D%E0%A4%9F%E0%A5%8B_%2F_%E0%A4%85%E0%A4%A8%E0%A4%BF%E0%A4%B2_%E0%A4%85%E0%A4%A8%E0%A4%B2%E0%A4%B9%E0%A4%BE%E0%A4%A4%E0%A5%81"},
    {"title": "ख़ुद अपनी ही प्रतीक्षा में", "poet": "वेणु गोपाल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%96%E0%A4%BC%E0%A5%81%E0%A4%A6_%E0%A4%85%E0%A4%AA%E0%A4%A8%E0%A5%80_%E0%A4%B9%E0%A5%80_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%A4%E0%A5%80%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A4%BE_%E0%A4%AE%E0%A5%87%E0%A4%82_%2F_%E0%A4%B5%E0%A5%87%E0%A4%A3%E0%A5%81_%E0%A4%97%E0%A5%8B%E0%A4%AA%E0%A4%BE%E0%A4%B2"},
    {"title": "नगर", "poet": "सुभाष काक", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A8%E0%A4%97%E0%A4%B0_%2F_%E0%A4%B8%E0%A5%81%E0%A4%AD%E0%A4%BE%E0%A4%B7_%E0%A4%95%E0%A4%BE%E0%A4%95"},
    {"title": "बारिश", "poet": "अदनान कफ़ील दरवेश", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A4%BE%E0%A4%B0%E0%A4%BF%E0%A4%B6_%2F_%E0%A4%85%E0%A4%A6%E0%A4%A8%E0%A4%BE%E0%A4%A8_%E0%A4%95%E0%A4%AB%E0%A4%BC%E0%A5%80%E0%A4%B2_%E0%A4%A6%E0%A4%B0%E0%A4%B5%E0%A5%87%E0%A4%B6"},
    {"title": "साच", "poet": "इरशाद अज़ीज़", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B8%E0%A4%BE%E0%A4%9A_%2F_%E0%A4%87%E0%A4%B0%E0%A4%B6%E0%A4%BE%E0%A4%A6_%E0%A4%85%E0%A4%9C%E0%A4%BC%E0%A5%80%E0%A4%9C%E0%A4%BC"},
    {"title": "था कहा \"शुक्र झांकता न मलिना उडुगण की चटकारी है", "poet": "प्रेम नारायण 'पंकिल'", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A5%E0%A4%BE_%E0%A4%95%E0%A4%B9%E0%A4%BE_%22%E0%A4%B6%E0%A5%81%E0%A4%95%E0%A5%8D%E0%A4%B0_%E0%A4%9D%E0%A4%BE%E0%A4%82%E0%A4%95%E0%A4%A4%E0%A4%BE_%E0%A4%A8_%E0%A4%AE%E0%A4%B2%E0%A4%BF%E0%A4%A8%E0%A4%BE_%E0%A4%89%E0%A4%A1%E0%A5%81%E0%A4%97%E0%A4%A3_%E0%A4%95%E0%A5%80_%E0%A4%9A%E0%A4%9F%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%80_%E0%A4%B9%E0%A5%88_%2F_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%AE_%E0%A4%A8%E0%A4%BE%E0%A4%B0%E0%A4%BE%E0%A4%AF%E0%A4%A3_%27%E0%A4%AA%E0%A4%82%E0%A4%95%E0%A4%BF%E0%A4%B2%27"},
    {"title": "विचित्र युद्ध", "poet": "इंदुशेखर तत्पुरुष", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B5%E0%A4%BF%E0%A4%9A%E0%A4%BF%E0%A4%A4%E0%A5%8D%E0%A4%B0_%E0%A4%AF%E0%A5%81%E0%A4%A6%E0%A5%8D%E0%A4%A7_%2F_%E0%A4%87%E0%A4%82%E0%A4%A6%E0%A5%81%E0%A4%B6%E0%A5%87%E0%A4%96%E0%A4%B0_%E0%A4%A4%E0%A4%A4%E0%A5%8D%E0%A4%AA%E0%A5%81%E0%A4%B0%E0%A5%81%E0%A4%B7"},
    {"title": "दाल बराबर याद रखना", "poet": "मनोज कुमार झा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A6%E0%A4%BE%E0%A4%B2_%E0%A4%AC%E0%A4%B0%E0%A4%BE%E0%A4%AC%E0%A4%B0_%E0%A4%AF%E0%A4%BE%E0%A4%A6_%E0%A4%B0%E0%A4%96%E0%A4%A8%E0%A4%BE_%2F_%E0%A4%AE%E0%A4%A8%E0%A5%8B%E0%A4%9C_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0_%E0%A4%9D%E0%A4%BE"},
    {"title": "जुहू नरेन्द्र जैन और कविता / बुद्ध", "poet": "नहा कर नही लौटा है बुद्ध", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9C%E0%A5%81%E0%A4%B9%E0%A5%82_%E0%A4%A8%E0%A4%B0%E0%A5%87%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%8D%E0%A4%B0_%E0%A4%9C%E0%A5%88%E0%A4%A8_%E0%A4%94%E0%A4%B0_%E0%A4%95%E0%A4%B5%E0%A4%BF%E0%A4%A4%E0%A4%BE_%2F_%E0%A4%AC%E0%A5%81%E0%A4%A6%E0%A5%8D%E0%A4%A7_%2F_%E0%A4%A8%E0%A4%B9%E0%A4%BE_%E0%A4%95%E0%A4%B0_%E0%A4%A8%E0%A4%B9%E0%A5%80_%E0%A4%B2%E0%A5%8C%E0%A4%9F%E0%A4%BE_%E0%A4%B9%E0%A5%88_%E0%A4%AC%E0%A5%81%E0%A4%A6%E0%A5%8D%E0%A4%A7"},
    {"title": "बन्द खिड़की की देह पर / जय गोस्वामी", "poet": "जयश्री पुरवार", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A4%A8%E0%A5%8D%E0%A4%A6_%E0%A4%96%E0%A4%BF%E0%A4%A1%E0%A4%BC%E0%A4%95%E0%A5%80_%E0%A4%95%E0%A5%80_%E0%A4%A6%E0%A5%87%E0%A4%B9_%E0%A4%AA%E0%A4%B0_%2F_%E0%A4%9C%E0%A4%AF_%E0%A4%97%E0%A5%8B%E0%A4%B8%E0%A5%8D%E0%A4%B5%E0%A4%BE%E0%A4%AE%E0%A5%80_%2F_%E0%A4%9C%E0%A4%AF%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80_%E0%A4%AA%E0%A5%81%E0%A4%B0%E0%A4%B5%E0%A4%BE%E0%A4%B0"},
    {"title": "प्यार", "poet": "ऋषभ देव शर्मा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AA%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%B0_%2F_%E0%A4%8B%E0%A4%B7%E0%A4%AD_%E0%A4%A6%E0%A5%87%E0%A4%B5_%E0%A4%B6%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE"},
    {"title": "कामरेड, तुम भी न!", "poet": "कुमार विमलेन्दु सिंह", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A4%BE%E0%A4%AE%E0%A4%B0%E0%A5%87%E0%A4%A1%2C_%E0%A4%A4%E0%A5%81%E0%A4%AE_%E0%A4%AD%E0%A5%80_%E0%A4%A8%21_%2F_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0_%E0%A4%B5%E0%A4%BF%E0%A4%AE%E0%A4%B2%E0%A5%87%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%81_%E0%A4%B8%E0%A4%BF%E0%A4%82%E0%A4%B9"},
    {"title": "दिलावन दिलावन", "poet": "रमणिका गुप्ता", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A6%E0%A4%BF%E0%A4%B2%E0%A4%BE%E0%A4%B5%E0%A4%A8_%E0%A4%A6%E0%A4%BF%E0%A4%B2%E0%A4%BE%E0%A4%B5%E0%A4%A8_%2F_%E0%A4%B0%E0%A4%AE%E0%A4%A3%E0%A4%BF%E0%A4%95%E0%A4%BE_%E0%A4%97%E0%A5%81%E0%A4%AA%E0%A5%8D%E0%A4%A4%E0%A4%BE"},
    {"title": "हिन्दी", "poet": "मनोज चारण 'कुमार'", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B9%E0%A4%BF%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%80_%2F_%E0%A4%AE%E0%A4%A8%E0%A5%8B%E0%A4%9C_%E0%A4%9A%E0%A4%BE%E0%A4%B0%E0%A4%A3_%27%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0%27"},
    {"title": "बाढ़", "poet": "रंजना जायसवाल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A4%BE%E0%A4%A2%E0%A4%BC_%2F_%E0%A4%B0%E0%A4%82%E0%A4%9C%E0%A4%A8%E0%A4%BE_%E0%A4%9C%E0%A4%BE%E0%A4%AF%E0%A4%B8%E0%A4%B5%E0%A4%BE%E0%A4%B2"},
    {"title": "यह प्यार", "poet": "अरुणा राय", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AF%E0%A4%B9_%E0%A4%AA%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%B0_%2F_%E0%A4%85%E0%A4%B0%E0%A5%81%E0%A4%A3%E0%A4%BE_%E0%A4%B0%E0%A4%BE%E0%A4%AF"},
    {"title": "रहरको शिखर", "poet": "ज्योति जङ्गल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B0%E0%A4%B9%E0%A4%B0%E0%A4%95%E0%A5%8B_%E0%A4%B6%E0%A4%BF%E0%A4%96%E0%A4%B0_%2F_%E0%A4%9C%E0%A5%8D%E0%A4%AF%E0%A5%8B%E0%A4%A4%E0%A4%BF_%E0%A4%9C%E0%A4%99%E0%A5%8D%E0%A4%97%E0%A4%B2"},
    {"title": "एक दहशतगर्द", "poet": "अनवर ईरज", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%8F%E0%A4%95_%E0%A4%A6%E0%A4%B9%E0%A4%B6%E0%A4%A4%E0%A4%97%E0%A4%B0%E0%A5%8D%E0%A4%A6_%2F_%E0%A4%85%E0%A4%A8%E0%A4%B5%E0%A4%B0_%E0%A4%88%E0%A4%B0%E0%A4%9C"},
    {"title": "वाणी की मूर्ति गढ़ रहा हूं", "poet": "रवीन्द्रनाथ ठाकुर", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B5%E0%A4%BE%E0%A4%A3%E0%A5%80_%E0%A4%95%E0%A5%80_%E0%A4%AE%E0%A5%82%E0%A4%B0%E0%A5%8D%E0%A4%A4%E0%A4%BF_%E0%A4%97%E0%A4%A2%E0%A4%BC_%E0%A4%B0%E0%A4%B9%E0%A4%BE_%E0%A4%B9%E0%A5%82%E0%A4%82_%2F_%E0%A4%B0%E0%A4%B5%E0%A5%80%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%8D%E0%A4%B0%E0%A4%A8%E0%A4%BE%E0%A4%A5_%E0%A4%A0%E0%A4%BE%E0%A4%95%E0%A5%81%E0%A4%B0"},
    {"title": "क्यों ?", "poet": "राग तेलंग", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A5%8D%E0%A4%AF%E0%A5%8B%E0%A4%82_%3F_%2F_%E0%A4%B0%E0%A4%BE%E0%A4%97_%E0%A4%A4%E0%A5%87%E0%A4%B2%E0%A4%82%E0%A4%97"},
    {"title": "मैडम-सरजी", "poet": "दीनदयाल शर्मा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A5%88%E0%A4%A1%E0%A4%AE-%E0%A4%B8%E0%A4%B0%E0%A4%9C%E0%A5%80_%2F_%E0%A4%A6%E0%A5%80%E0%A4%A8%E0%A4%A6%E0%A4%AF%E0%A4%BE%E0%A4%B2_%E0%A4%B6%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE"},
    {"title": "कबूतर और मैं (4)", "poet": "प्रताप सहगल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A4%AC%E0%A5%82%E0%A4%A4%E0%A4%B0_%E0%A4%94%E0%A4%B0_%E0%A4%AE%E0%A5%88%E0%A4%82_%284%29_%2F_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%A4%E0%A4%BE%E0%A4%AA_%E0%A4%B8%E0%A4%B9%E0%A4%97%E0%A4%B2"},
    {"title": "जयप्रकाश / सामधेनी", "poet": "रामधारी सिंह \"दिनकर\"", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9C%E0%A4%AF%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%95%E0%A4%BE%E0%A4%B6_%2F_%E0%A4%B8%E0%A4%BE%E0%A4%AE%E0%A4%A7%E0%A5%87%E0%A4%A8%E0%A5%80_%2F_%E0%A4%B0%E0%A4%BE%E0%A4%AE%E0%A4%A7%E0%A4%BE%E0%A4%B0%E0%A5%80_%E0%A4%B8%E0%A4%BF%E0%A4%82%E0%A4%B9_%22%E0%A4%A6%E0%A4%BF%E0%A4%A8%E0%A4%95%E0%A4%B0%22"},
    {"title": "\"आख़िरी\"", "poet": "रति सक्सेना", "url": "https://kavitakosh.org/kk/index.php?title=%22%E0%A4%86%E0%A4%96%E0%A4%BC%E0%A4%BF%E0%A4%B0%E0%A5%80%22_%2F_%E0%A4%B0%E0%A4%A4%E0%A4%BF_%E0%A4%B8%E0%A4%95%E0%A5%8D%E0%A4%B8%E0%A5%87%E0%A4%A8%E0%A4%BE"},
    {"title": "जे ते गजगौनी के नितँब हैँ विशद होत", "poet": "अज्ञात कवि (रीतिकाल)", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9C%E0%A5%87_%E0%A4%A4%E0%A5%87_%E0%A4%97%E0%A4%9C%E0%A4%97%E0%A5%8C%E0%A4%A8%E0%A5%80_%E0%A4%95%E0%A5%87_%E0%A4%A8%E0%A4%BF%E0%A4%A4%E0%A4%81%E0%A4%AC_%E0%A4%B9%E0%A5%88%E0%A4%81_%E0%A4%B5%E0%A4%BF%E0%A4%B6%E0%A4%A6_%E0%A4%B9%E0%A5%8B%E0%A4%A4_%2F_%E0%A4%85%E0%A4%9C%E0%A5%8D%E0%A4%9E%E0%A4%BE%E0%A4%A4_%E0%A4%95%E0%A4%B5%E0%A4%BF_%28%E0%A4%B0%E0%A5%80%E0%A4%A4%E0%A4%BF%E0%A4%95%E0%A4%BE%E0%A4%B2%29"},
    {"title": "चाँद मेरा", "poet": "अंकिता कुलश्रेष्ठ", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9A%E0%A4%BE%E0%A4%81%E0%A4%A6_%E0%A4%AE%E0%A5%87%E0%A4%B0%E0%A4%BE_%2F_%E0%A4%85%E0%A4%82%E0%A4%95%E0%A4%BF%E0%A4%A4%E0%A4%BE_%E0%A4%95%E0%A5%81%E0%A4%B2%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%B7%E0%A5%8D%E0%A4%A0"},
    {"title": "कुण्डलाकार विचार", "poet": "कात्यायनी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A5%81%E0%A4%A3%E0%A5%8D%E0%A4%A1%E0%A4%B2%E0%A4%BE%E0%A4%95%E0%A4%BE%E0%A4%B0_%E0%A4%B5%E0%A4%BF%E0%A4%9A%E0%A4%BE%E0%A4%B0_%2F_%E0%A4%95%E0%A4%BE%E0%A4%A4%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%AF%E0%A4%A8%E0%A5%80"},
    {"title": "जद-जद पड़ै काळ", "poet": "नीरज दइया", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9C%E0%A4%A6-%E0%A4%9C%E0%A4%A6_%E0%A4%AA%E0%A4%A1%E0%A4%BC%E0%A5%88_%E0%A4%95%E0%A4%BE%E0%A4%B3_%2F_%E0%A4%A8%E0%A5%80%E0%A4%B0%E0%A4%9C_%E0%A4%A6%E0%A4%87%E0%A4%AF%E0%A4%BE"},
    {"title": "इंद्रावती की यात्रा", "poet": "शरद चन्द्र गौड़", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%87%E0%A4%82%E0%A4%A6%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%B5%E0%A4%A4%E0%A5%80_%E0%A4%95%E0%A5%80_%E0%A4%AF%E0%A4%BE%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BE_%2F_%E0%A4%B6%E0%A4%B0%E0%A4%A6_%E0%A4%9A%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%8D%E0%A4%B0_%E0%A4%97%E0%A5%8C%E0%A4%A1%E0%A4%BC"},
    {"title": "स्मृति की झील", "poet": "अनूप सेठी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B8%E0%A5%8D%E0%A4%AE%E0%A5%83%E0%A4%A4%E0%A4%BF_%E0%A4%95%E0%A5%80_%E0%A4%9D%E0%A5%80%E0%A4%B2_%2F_%E0%A4%85%E0%A4%A8%E0%A5%82%E0%A4%AA_%E0%A4%B8%E0%A5%87%E0%A4%A0%E0%A5%80"},
    {"title": "सैंतीस", "poet": "प्रमोद कुमार शर्मा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B8%E0%A5%88%E0%A4%82%E0%A4%A4%E0%A5%80%E0%A4%B8_%2F_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AE%E0%A5%8B%E0%A4%A6_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0_%E0%A4%B6%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE"},
    {"title": "मोबाइल", "poet": "निरंजन श्रोत्रिय", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A5%8B%E0%A4%AC%E0%A4%BE%E0%A4%87%E0%A4%B2_%2F_%E0%A4%A8%E0%A4%BF%E0%A4%B0%E0%A4%82%E0%A4%9C%E0%A4%A8_%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%8B%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF"},
    {"title": "साँझ की बात", "poet": "नरेन्द्र शर्मा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B8%E0%A4%BE%E0%A4%81%E0%A4%9D_%E0%A4%95%E0%A5%80_%E0%A4%AC%E0%A4%BE%E0%A4%A4_%2F_%E0%A4%A8%E0%A4%B0%E0%A5%87%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%8D%E0%A4%B0_%E0%A4%B6%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE"},
    {"title": "फर्क-1", "poet": "भरत ओला", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AB%E0%A4%B0%E0%A5%8D%E0%A4%95-1_%2F_%E0%A4%AD%E0%A4%B0%E0%A4%A4_%E0%A4%93%E0%A4%B2%E0%A4%BE"},
    {"title": "मनौती", "poet": "प्रतिभा सक्सेना", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A4%A8%E0%A5%8C%E0%A4%A4%E0%A5%80_%2F_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%A4%E0%A4%BF%E0%A4%AD%E0%A4%BE_%E0%A4%B8%E0%A4%95%E0%A5%8D%E0%A4%B8%E0%A5%87%E0%A4%A8%E0%A4%BE"},
    {"title": "एक बूढ़ी दादी", "poet": "अनुभूति गुप्ता", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%8F%E0%A4%95_%E0%A4%AC%E0%A5%82%E0%A4%A2%E0%A4%BC%E0%A5%80_%E0%A4%A6%E0%A4%BE%E0%A4%A6%E0%A5%80_%2F_%E0%A4%85%E0%A4%A8%E0%A5%81%E0%A4%AD%E0%A5%82%E0%A4%A4%E0%A4%BF_%E0%A4%97%E0%A5%81%E0%A4%AA%E0%A5%8D%E0%A4%A4%E0%A4%BE"},
    {"title": "ऊँचा-ऊँचा पाबत, तहिं वसै सबरी वाला", "poet": "सरहपा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%8A%E0%A4%81%E0%A4%9A%E0%A4%BE-%E0%A4%8A%E0%A4%81%E0%A4%9A%E0%A4%BE_%E0%A4%AA%E0%A4%BE%E0%A4%AC%E0%A4%A4%2C_%E0%A4%A4%E0%A4%B9%E0%A4%BF%E0%A4%82_%E0%A4%B5%E0%A4%B8%E0%A5%88_%E0%A4%B8%E0%A4%AC%E0%A4%B0%E0%A5%80_%E0%A4%B5%E0%A4%BE%E0%A4%B2%E0%A4%BE_%2F_%E0%A4%B8%E0%A4%B0%E0%A4%B9%E0%A4%AA%E0%A4%BE"},
    {"title": "अभावों की यात्रा", "poet": "महेश सन्तोषी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%85%E0%A4%AD%E0%A4%BE%E0%A4%B5%E0%A5%8B%E0%A4%82_%E0%A4%95%E0%A5%80_%E0%A4%AF%E0%A4%BE%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BE_%2F_%E0%A4%AE%E0%A4%B9%E0%A5%87%E0%A4%B6_%E0%A4%B8%E0%A4%A8%E0%A5%8D%E0%A4%A4%E0%A5%8B%E0%A4%B7%E0%A5%80"},
    {"title": "जुत्ता", "poet": "विमल निभा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9C%E0%A5%81%E0%A4%A4%E0%A5%8D%E0%A4%A4%E0%A4%BE_%2F_%E0%A4%B5%E0%A4%BF%E0%A4%AE%E0%A4%B2_%E0%A4%A8%E0%A4%BF%E0%A4%AD%E0%A4%BE"},
    {"title": "तुम / विहान", "poet": "महेन्द्र भटनागर", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A4%E0%A5%81%E0%A4%AE_%2F_%E0%A4%B5%E0%A4%BF%E0%A4%B9%E0%A4%BE%E0%A4%A8_%2F_%E0%A4%AE%E0%A4%B9%E0%A5%87%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%8D%E0%A4%B0_%E0%A4%AD%E0%A4%9F%E0%A4%A8%E0%A4%BE%E0%A4%97%E0%A4%B0"},
    {"title": "मैं कहीं नहीं मिलता आजकल", "poet": "अजय कुमार", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A5%88%E0%A4%82_%E0%A4%95%E0%A4%B9%E0%A5%80%E0%A4%82_%E0%A4%A8%E0%A4%B9%E0%A5%80%E0%A4%82_%E0%A4%AE%E0%A4%BF%E0%A4%B2%E0%A4%A4%E0%A4%BE_%E0%A4%86%E0%A4%9C%E0%A4%95%E0%A4%B2_%2F_%E0%A4%85%E0%A4%9C%E0%A4%AF_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0"},
    {"title": "सान्निध्य", "poet": "विमलेश शर्मा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B8%E0%A4%BE%E0%A4%A8%E0%A5%8D%E0%A4%A8%E0%A4%BF%E0%A4%A7%E0%A5%8D%E0%A4%AF_%2F_%E0%A4%B5%E0%A4%BF%E0%A4%AE%E0%A4%B2%E0%A5%87%E0%A4%B6_%E0%A4%B6%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE"},
    {"title": "इतिसिद्धम्", "poet": "विमलेश शर्मा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%87%E0%A4%A4%E0%A4%BF%E0%A4%B8%E0%A4%BF%E0%A4%A6%E0%A5%8D%E0%A4%A7%E0%A4%AE%E0%A5%8D_%2F_%E0%A4%B5%E0%A4%BF%E0%A4%AE%E0%A4%B2%E0%A5%87%E0%A4%B6_%E0%A4%B6%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE"},
    {"title": "बैठ हम नदिया किनारे ध्यान में उलझे रहे", "poet": "पुष्पराज यादव", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A5%88%E0%A4%A0_%E0%A4%B9%E0%A4%AE_%E0%A4%A8%E0%A4%A6%E0%A4%BF%E0%A4%AF%E0%A4%BE_%E0%A4%95%E0%A4%BF%E0%A4%A8%E0%A4%BE%E0%A4%B0%E0%A5%87_%E0%A4%A7%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%A8_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%89%E0%A4%B2%E0%A4%9D%E0%A5%87_%E0%A4%B0%E0%A4%B9%E0%A5%87_%2F_%E0%A4%AA%E0%A5%81%E0%A4%B7%E0%A5%8D%E0%A4%AA%E0%A4%B0%E0%A4%BE%E0%A4%9C_%E0%A4%AF%E0%A4%BE%E0%A4%A6%E0%A4%B5"},
    {"title": "लड़की / एज़रा पाउंड", "poet": "एम० एस० पटेल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B2%E0%A4%A1%E0%A4%BC%E0%A4%95%E0%A5%80_%2F_%E0%A4%8F%E0%A4%9C%E0%A4%BC%E0%A4%B0%E0%A4%BE_%E0%A4%AA%E0%A4%BE%E0%A4%89%E0%A4%82%E0%A4%A1_%2F_%E0%A4%8F%E0%A4%AE%E0%A5%A6_%E0%A4%8F%E0%A4%B8%E0%A5%A6_%E0%A4%AA%E0%A4%9F%E0%A5%87%E0%A4%B2"},
    {"title": "कविता", "poet": "विद्यानाथ पोख्रेल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A4%B5%E0%A4%BF%E0%A4%A4%E0%A4%BE_%2F_%E0%A4%B5%E0%A4%BF%E0%A4%A6%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%A8%E0%A4%BE%E0%A4%A5_%E0%A4%AA%E0%A5%8B%E0%A4%96%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%B2"},
    {"title": "पैन", "poet": "हरीश हैरी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AA%E0%A5%88%E0%A4%A8_%2F_%E0%A4%B9%E0%A4%B0%E0%A5%80%E0%A4%B6_%E0%A4%B9%E0%A5%88%E0%A4%B0%E0%A5%80"},
    {"title": "आश्वस्ति", "poet": "अज्ञेय", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%86%E0%A4%B6%E0%A5%8D%E0%A4%B5%E0%A4%B8%E0%A5%8D%E0%A4%A4%E0%A4%BF_%2F_%E0%A4%85%E0%A4%9C%E0%A5%8D%E0%A4%9E%E0%A5%87%E0%A4%AF"},
    {"title": "यातनाएँ बोलतीं हैं", "poet": "कल्पना पंत", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AF%E0%A4%BE%E0%A4%A4%E0%A4%A8%E0%A4%BE%E0%A4%8F%E0%A4%81_%E0%A4%AC%E0%A5%8B%E0%A4%B2%E0%A4%A4%E0%A5%80%E0%A4%82_%E0%A4%B9%E0%A5%88%E0%A4%82_%2F_%E0%A4%95%E0%A4%B2%E0%A5%8D%E0%A4%AA%E0%A4%A8%E0%A4%BE_%E0%A4%AA%E0%A4%82%E0%A4%A4"},
    {"title": "कविता से / अलेक्सान्दर ब्लोक", "poet": "वरयाम सिंह", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A4%B5%E0%A4%BF%E0%A4%A4%E0%A4%BE_%E0%A4%B8%E0%A5%87_%2F_%E0%A4%85%E0%A4%B2%E0%A5%87%E0%A4%95%E0%A5%8D%E0%A4%B8%E0%A4%BE%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A4%B0_%E0%A4%AC%E0%A5%8D%E0%A4%B2%E0%A5%8B%E0%A4%95_%2F_%E0%A4%B5%E0%A4%B0%E0%A4%AF%E0%A4%BE%E0%A4%AE_%E0%A4%B8%E0%A4%BF%E0%A4%82%E0%A4%B9"},
    {"title": "चलत स्यामघन राजत, बाजति पैंजनि पग-पग चारु मनोहर", "poet": "सूरदास", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9A%E0%A4%B2%E0%A4%A4_%E0%A4%B8%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%AE%E0%A4%98%E0%A4%A8_%E0%A4%B0%E0%A4%BE%E0%A4%9C%E0%A4%A4%2C_%E0%A4%AC%E0%A4%BE%E0%A4%9C%E0%A4%A4%E0%A4%BF_%E0%A4%AA%E0%A5%88%E0%A4%82%E0%A4%9C%E0%A4%A8%E0%A4%BF_%E0%A4%AA%E0%A4%97-%E0%A4%AA%E0%A4%97_%E0%A4%9A%E0%A4%BE%E0%A4%B0%E0%A5%81_%E0%A4%AE%E0%A4%A8%E0%A5%8B%E0%A4%B9%E0%A4%B0_%2F_%E0%A4%B8%E0%A5%82%E0%A4%B0%E0%A4%A6%E0%A4%BE%E0%A4%B8"},
    {"title": "मुक्तक-13", "poet": "रंजना वर्मा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A5%81%E0%A4%95%E0%A5%8D%E0%A4%A4%E0%A4%95-13_%2F_%E0%A4%B0%E0%A4%82%E0%A4%9C%E0%A4%A8%E0%A4%BE_%E0%A4%B5%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE"},
    {"title": "समय में मोड़", "poet": "नवनीता कानूनगो", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B8%E0%A4%AE%E0%A4%AF_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%AE%E0%A5%8B%E0%A4%A1%E0%A4%BC_%2F_%E0%A4%A8%E0%A4%B5%E0%A4%A8%E0%A5%80%E0%A4%A4%E0%A4%BE_%E0%A4%95%E0%A4%BE%E0%A4%A8%E0%A5%82%E0%A4%A8%E0%A4%97%E0%A5%8B"},
    {"title": "निगल रही है अब यह पीढ़ी", "poet": "राजकुमारी रश्मि", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A8%E0%A4%BF%E0%A4%97%E0%A4%B2_%E0%A4%B0%E0%A4%B9%E0%A5%80_%E0%A4%B9%E0%A5%88_%E0%A4%85%E0%A4%AC_%E0%A4%AF%E0%A4%B9_%E0%A4%AA%E0%A5%80%E0%A4%A2%E0%A4%BC%E0%A5%80_%2F_%E0%A4%B0%E0%A4%BE%E0%A4%9C%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0%E0%A5%80_%E0%A4%B0%E0%A4%B6%E0%A5%8D%E0%A4%AE%E0%A4%BF"},
    {"title": "आलोक", "poet": "केशव", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%86%E0%A4%B2%E0%A5%8B%E0%A4%95_%2F_%E0%A4%95%E0%A5%87%E0%A4%B6%E0%A4%B5"},
    {"title": "मुझे प्रेरणा दे तो कौन?", "poet": "रामगोपाल 'रुद्र'", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A5%81%E0%A4%9D%E0%A5%87_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%B0%E0%A4%A3%E0%A4%BE_%E0%A4%A6%E0%A5%87_%E0%A4%A4%E0%A5%8B_%E0%A4%95%E0%A5%8C%E0%A4%A8%3F_%2F_%E0%A4%B0%E0%A4%BE%E0%A4%AE%E0%A4%97%E0%A5%8B%E0%A4%AA%E0%A4%BE%E0%A4%B2_%27%E0%A4%B0%E0%A5%81%E0%A4%A6%E0%A5%8D%E0%A4%B0%27"},
    {"title": "बदलती रही स्त्रित्राँ", "poet": "परितोष कुमार 'पीयूष'", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A4%A6%E0%A4%B2%E0%A4%A4%E0%A5%80_%E0%A4%B0%E0%A4%B9%E0%A5%80_%E0%A4%B8%E0%A5%8D%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%81_%2F_%E0%A4%AA%E0%A4%B0%E0%A4%BF%E0%A4%A4%E0%A5%8B%E0%A4%B7_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0_%27%E0%A4%AA%E0%A5%80%E0%A4%AF%E0%A5%82%E0%A4%B7%27"},
    {"title": "पौरुष", "poet": "ज्योतीन्द्र प्रसाद झा 'पंकज'", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AA%E0%A5%8C%E0%A4%B0%E0%A5%81%E0%A4%B7_%2F_%E0%A4%9C%E0%A5%8D%E0%A4%AF%E0%A5%8B%E0%A4%A4%E0%A5%80%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%8D%E0%A4%B0_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B8%E0%A4%BE%E0%A4%A6_%E0%A4%9D%E0%A4%BE_%27%E0%A4%AA%E0%A4%82%E0%A4%95%E0%A4%9C%27"},
    {"title": "म्हैं सोचूं", "poet": "वाज़िद हसन काज़ी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A5%8D%E0%A4%B9%E0%A5%88%E0%A4%82_%E0%A4%B8%E0%A5%8B%E0%A4%9A%E0%A5%82%E0%A4%82_%2F_%E0%A4%B5%E0%A4%BE%E0%A4%9C%E0%A4%BC%E0%A4%BF%E0%A4%A6_%E0%A4%B9%E0%A4%B8%E0%A4%A8_%E0%A4%95%E0%A4%BE%E0%A4%9C%E0%A4%BC%E0%A5%80"},
    {"title": "आशी:", "poet": "अज्ञेय", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%86%E0%A4%B6%E0%A5%80%3A_%2F_%E0%A4%85%E0%A4%9C%E0%A5%8D%E0%A4%9E%E0%A5%87%E0%A4%AF"},
    {"title": "प्रेम और स्पर्श", "poet": "अमिता प्रजापति", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%AE_%E0%A4%94%E0%A4%B0_%E0%A4%B8%E0%A5%8D%E0%A4%AA%E0%A4%B0%E0%A5%8D%E0%A4%B6_%2F_%E0%A4%85%E0%A4%AE%E0%A4%BF%E0%A4%A4%E0%A4%BE_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%9C%E0%A4%BE%E0%A4%AA%E0%A4%A4%E0%A4%BF"},
    {"title": "माला", "poet": "कालीकान्त झा ‘बूच’", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A4%BE%E0%A4%B2%E0%A4%BE_%2F_%E0%A4%95%E0%A4%BE%E0%A4%B2%E0%A5%80%E0%A4%95%E0%A4%BE%E0%A4%A8%E0%A5%8D%E0%A4%A4_%E0%A4%9D%E0%A4%BE_%E2%80%98%E0%A4%AC%E0%A5%82%E0%A4%9A%E2%80%99"},
    {"title": "आँखों का आकर्षण", "poet": "रामनरेश त्रिपाठी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%86%E0%A4%81%E0%A4%96%E0%A5%8B%E0%A4%82_%E0%A4%95%E0%A4%BE_%E0%A4%86%E0%A4%95%E0%A4%B0%E0%A5%8D%E0%A4%B7%E0%A4%A3_%2F_%E0%A4%B0%E0%A4%BE%E0%A4%AE%E0%A4%A8%E0%A4%B0%E0%A5%87%E0%A4%B6_%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AA%E0%A4%BE%E0%A4%A0%E0%A5%80"},
    {"title": "वे", "poet": "कुमार अनुपम", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B5%E0%A5%87_%2F_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0_%E0%A4%85%E0%A4%A8%E0%A5%81%E0%A4%AA%E0%A4%AE"},
    {"title": "मौसम का डाकिया", "poet": "शशि पाधा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A5%8C%E0%A4%B8%E0%A4%AE_%E0%A4%95%E0%A4%BE_%E0%A4%A1%E0%A4%BE%E0%A4%95%E0%A4%BF%E0%A4%AF%E0%A4%BE_%2F_%E0%A4%B6%E0%A4%B6%E0%A4%BF_%E0%A4%AA%E0%A4%BE%E0%A4%A7%E0%A4%BE"},
    {"title": "किंछा", "poet": "राकेश रवि", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A4%BF%E0%A4%82%E0%A4%9B%E0%A4%BE_%2F_%E0%A4%B0%E0%A4%BE%E0%A4%95%E0%A5%87%E0%A4%B6_%E0%A4%B0%E0%A4%B5%E0%A4%BF"},
    {"title": "मां: 1", "poet": "मीठेश निर्मोही", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A4%BE%E0%A4%82%3A_1_%2F_%E0%A4%AE%E0%A5%80%E0%A4%A0%E0%A5%87%E0%A4%B6_%E0%A4%A8%E0%A4%BF%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A5%8B%E0%A4%B9%E0%A5%80"},
    {"title": "तेरा चेहरा", "poet": "अनातोली परपरा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A4%E0%A5%87%E0%A4%B0%E0%A4%BE_%E0%A4%9A%E0%A5%87%E0%A4%B9%E0%A4%B0%E0%A4%BE_%2F_%E0%A4%85%E0%A4%A8%E0%A4%BE%E0%A4%A4%E0%A5%8B%E0%A4%B2%E0%A5%80_%E0%A4%AA%E0%A4%B0%E0%A4%AA%E0%A4%B0%E0%A4%BE"},
    {"title": "अफसोस", "poet": "प्रिया जौहरी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%85%E0%A4%AB%E0%A4%B8%E0%A5%8B%E0%A4%B8_%2F_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF%E0%A4%BE_%E0%A4%9C%E0%A5%8C%E0%A4%B9%E0%A4%B0%E0%A5%80"},
    {"title": "बिन कहे", "poet": "आनंद कुमार द्विवेदी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A4%BF%E0%A4%A8_%E0%A4%95%E0%A4%B9%E0%A5%87_%2F_%E0%A4%86%E0%A4%A8%E0%A4%82%E0%A4%A6_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0_%E0%A4%A6%E0%A5%8D%E0%A4%B5%E0%A4%BF%E0%A4%B5%E0%A5%87%E0%A4%A6%E0%A5%80"},
    {"title": "दुविधा", "poet": "कुमार कृष्ण", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A6%E0%A5%81%E0%A4%B5%E0%A4%BF%E0%A4%A7%E0%A4%BE_%2F_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0_%E0%A4%95%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A3"},
    {"title": "शंकराचार्यले जलाएको म बौद्धग्रन्थ हुँँ", "poet": "उपेन्द्र श्रेष्ठ", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B6%E0%A4%82%E0%A4%95%E0%A4%B0%E0%A4%BE%E0%A4%9A%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%E0%A4%B2%E0%A5%87_%E0%A4%9C%E0%A4%B2%E0%A4%BE%E0%A4%8F%E0%A4%95%E0%A5%8B_%E0%A4%AE_%E0%A4%AC%E0%A5%8C%E0%A4%A6%E0%A5%8D%E0%A4%A7%E0%A4%97%E0%A5%8D%E0%A4%B0%E0%A4%A8%E0%A5%8D%E0%A4%A5_%E0%A4%B9%E0%A5%81%E0%A4%81%E0%A4%81_%2F_%E0%A4%89%E0%A4%AA%E0%A5%87%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%8D%E0%A4%B0_%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%B7%E0%A5%8D%E0%A4%A0"},
    {"title": "चम्पई आकाश तुम हो", "poet": "केदारनाथ अग्रवाल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9A%E0%A4%AE%E0%A5%8D%E0%A4%AA%E0%A4%88_%E0%A4%86%E0%A4%95%E0%A4%BE%E0%A4%B6_%E0%A4%A4%E0%A5%81%E0%A4%AE_%E0%A4%B9%E0%A5%8B_%2F_%E0%A4%95%E0%A5%87%E0%A4%A6%E0%A4%BE%E0%A4%B0%E0%A4%A8%E0%A4%BE%E0%A4%A5_%E0%A4%85%E0%A4%97%E0%A5%8D%E0%A4%B0%E0%A4%B5%E0%A4%BE%E0%A4%B2"},
    {"title": "अनगढ़ मैदान थे पिता", "poet": "भरत प्रसाद", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%85%E0%A4%A8%E0%A4%97%E0%A4%A2%E0%A4%BC_%E0%A4%AE%E0%A5%88%E0%A4%A6%E0%A4%BE%E0%A4%A8_%E0%A4%A5%E0%A5%87_%E0%A4%AA%E0%A4%BF%E0%A4%A4%E0%A4%BE_%2F_%E0%A4%AD%E0%A4%B0%E0%A4%A4_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B8%E0%A4%BE%E0%A4%A6"},
    {"title": "सड़क", "poet": "रेणु हुसैन", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B8%E0%A4%A1%E0%A4%BC%E0%A4%95_%2F_%E0%A4%B0%E0%A5%87%E0%A4%A3%E0%A5%81_%E0%A4%B9%E0%A5%81%E0%A4%B8%E0%A5%88%E0%A4%A8"},
    {"title": "द्रुपद सुता-खण्ड-03", "poet": "रंजना वर्मा", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A6%E0%A5%8D%E0%A4%B0%E0%A5%81%E0%A4%AA%E0%A4%A6_%E0%A4%B8%E0%A5%81%E0%A4%A4%E0%A4%BE-%E0%A4%96%E0%A4%A3%E0%A5%8D%E0%A4%A1-03_%2F_%E0%A4%B0%E0%A4%82%E0%A4%9C%E0%A4%A8%E0%A4%BE_%E0%A4%B5%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE"},
    {"title": "बाँसुरी की फूँक", "poet": "नन्दकिशोर नवल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A4%BE%E0%A4%81%E0%A4%B8%E0%A5%81%E0%A4%B0%E0%A5%80_%E0%A4%95%E0%A5%80_%E0%A4%AB%E0%A5%82%E0%A4%81%E0%A4%95_%2F_%E0%A4%A8%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A4%95%E0%A4%BF%E0%A4%B6%E0%A5%8B%E0%A4%B0_%E0%A4%A8%E0%A4%B5%E0%A4%B2"},
    {"title": "स्त्री और घर", "poet": "गीताश्री", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B8%E0%A5%8D%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A5%80_%E0%A4%94%E0%A4%B0_%E0%A4%98%E0%A4%B0_%2F_%E0%A4%97%E0%A5%80%E0%A4%A4%E0%A4%BE%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80"},
    {"title": "गिरे तो क्या हुआ", "poet": "रविकान्त", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%97%E0%A4%BF%E0%A4%B0%E0%A5%87_%E0%A4%A4%E0%A5%8B_%E0%A4%95%E0%A5%8D%E0%A4%AF%E0%A4%BE_%E0%A4%B9%E0%A5%81%E0%A4%86_%2F_%E0%A4%B0%E0%A4%B5%E0%A4%BF%E0%A4%95%E0%A4%BE%E0%A4%A8%E0%A5%8D%E0%A4%A4"},
    {"title": "अंधकार / कुहकी कोयल खड़े पेड़ की देह", "poet": "केदारनाथ अग्रवाल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%85%E0%A4%82%E0%A4%A7%E0%A4%95%E0%A4%BE%E0%A4%B0_%2F_%E0%A4%95%E0%A5%81%E0%A4%B9%E0%A4%95%E0%A5%80_%E0%A4%95%E0%A5%8B%E0%A4%AF%E0%A4%B2_%E0%A4%96%E0%A4%A1%E0%A4%BC%E0%A5%87_%E0%A4%AA%E0%A5%87%E0%A4%A1%E0%A4%BC_%E0%A4%95%E0%A5%80_%E0%A4%A6%E0%A5%87%E0%A4%B9_%2F_%E0%A4%95%E0%A5%87%E0%A4%A6%E0%A4%BE%E0%A4%B0%E0%A4%A8%E0%A4%BE%E0%A4%A5_%E0%A4%85%E0%A4%97%E0%A5%8D%E0%A4%B0%E0%A4%B5%E0%A4%BE%E0%A4%B2"},
    {"title": "चील / सुकान्त भट्टाचार्य", "poet": "उत्पल बैनर्जी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9A%E0%A5%80%E0%A4%B2_%2F_%E0%A4%B8%E0%A5%81%E0%A4%95%E0%A4%BE%E0%A4%A8%E0%A5%8D%E0%A4%A4_%E0%A4%AD%E0%A4%9F%E0%A5%8D%E0%A4%9F%E0%A4%BE%E0%A4%9A%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF_%2F_%E0%A4%89%E0%A4%A4%E0%A5%8D%E0%A4%AA%E0%A4%B2_%E0%A4%AC%E0%A5%88%E0%A4%A8%E0%A4%B0%E0%A5%8D%E0%A4%9C%E0%A5%80"},
    {"title": "यह है माया को संसार!", "poet": "राधेश्याम ‘प्रवासी’", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AF%E0%A4%B9_%E0%A4%B9%E0%A5%88_%E0%A4%AE%E0%A4%BE%E0%A4%AF%E0%A4%BE_%E0%A4%95%E0%A5%8B_%E0%A4%B8%E0%A4%82%E0%A4%B8%E0%A4%BE%E0%A4%B0%21_%2F_%E0%A4%B0%E0%A4%BE%E0%A4%A7%E0%A5%87%E0%A4%B6%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%AE_%E2%80%98%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B5%E0%A4%BE%E0%A4%B8%E0%A5%80%E2%80%99"},
    {"title": "बुआ को सोचते हुए", "poet": "अर्पण कुमार", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AC%E0%A5%81%E0%A4%86_%E0%A4%95%E0%A5%8B_%E0%A4%B8%E0%A5%8B%E0%A4%9A%E0%A4%A4%E0%A5%87_%E0%A4%B9%E0%A5%81%E0%A4%8F_%2F_%E0%A4%85%E0%A4%B0%E0%A5%8D%E0%A4%AA%E0%A4%A3_%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A4%BE%E0%A4%B0"},
    {"title": "जीवन-मृत्यु", "poet": "पल्लवी त्रिवेदी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9C%E0%A5%80%E0%A4%B5%E0%A4%A8-%E0%A4%AE%E0%A5%83%E0%A4%A4%E0%A5%8D%E0%A4%AF%E0%A5%81_%2F_%E0%A4%AA%E0%A4%B2%E0%A5%8D%E0%A4%B2%E0%A4%B5%E0%A5%80_%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%B5%E0%A5%87%E0%A4%A6%E0%A5%80"},
    {"title": "मेरे रूप में तुम ही होगे", "poet": "उर्मिल सत्यभूषण", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%AE%E0%A5%87%E0%A4%B0%E0%A5%87_%E0%A4%B0%E0%A5%82%E0%A4%AA_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%A4%E0%A5%81%E0%A4%AE_%E0%A4%B9%E0%A5%80_%E0%A4%B9%E0%A5%8B%E0%A4%97%E0%A5%87_%2F_%E0%A4%89%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BF%E0%A4%B2_%E0%A4%B8%E0%A4%A4%E0%A5%8D%E0%A4%AF%E0%A4%AD%E0%A5%82%E0%A4%B7%E0%A4%A3"},
    {"title": "आज रंग है", "poet": "भव्य भसीन", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%86%E0%A4%9C_%E0%A4%B0%E0%A4%82%E0%A4%97_%E0%A4%B9%E0%A5%88_%2F_%E0%A4%AD%E0%A4%B5%E0%A5%8D%E0%A4%AF_%E0%A4%AD%E0%A4%B8%E0%A5%80%E0%A4%A8"},
    {"title": "टोक-डण्डा", "poet": "कन्हैयालाल मत्त", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%9F%E0%A5%8B%E0%A4%95-%E0%A4%A1%E0%A4%A3%E0%A5%8D%E0%A4%A1%E0%A4%BE_%2F_%E0%A4%95%E0%A4%A8%E0%A5%8D%E0%A4%B9%E0%A5%88%E0%A4%AF%E0%A4%BE%E0%A4%B2%E0%A4%BE%E0%A4%B2_%E0%A4%AE%E0%A4%A4%E0%A5%8D%E0%A4%A4"},
    {"title": "हमारी माँएँ पितृसत्ता के घोर षड्यन्त्र में फँसी हुई हैं", "poet": "नेहा नरुका", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B9%E0%A4%AE%E0%A4%BE%E0%A4%B0%E0%A5%80_%E0%A4%AE%E0%A4%BE%E0%A4%81%E0%A4%8F%E0%A4%81_%E0%A4%AA%E0%A4%BF%E0%A4%A4%E0%A5%83%E0%A4%B8%E0%A4%A4%E0%A5%8D%E0%A4%A4%E0%A4%BE_%E0%A4%95%E0%A5%87_%E0%A4%98%E0%A5%8B%E0%A4%B0_%E0%A4%B7%E0%A4%A1%E0%A5%8D%E0%A4%AF%E0%A4%A8%E0%A5%8D%E0%A4%A4%E0%A5%8D%E0%A4%B0_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%AB%E0%A4%81%E0%A4%B8%E0%A5%80_%E0%A4%B9%E0%A5%81%E0%A4%88_%E0%A4%B9%E0%A5%88%E0%A4%82_%2F_%E0%A4%A8%E0%A5%87%E0%A4%B9%E0%A4%BE_%E0%A4%A8%E0%A4%B0%E0%A5%81%E0%A4%95%E0%A4%BE"},
    {"title": "कौरव कौन, कौन पांडव", "poet": "अटल बिहारी वाजपेयी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%95%E0%A5%8C%E0%A4%B0%E0%A4%B5_%E0%A4%95%E0%A5%8C%E0%A4%A8%2C_%E0%A4%95%E0%A5%8C%E0%A4%A8_%E0%A4%AA%E0%A4%BE%E0%A4%82%E0%A4%A1%E0%A4%B5_%2F_%E0%A4%85%E0%A4%9F%E0%A4%B2_%E0%A4%AC%E0%A4%BF%E0%A4%B9%E0%A4%BE%E0%A4%B0%E0%A5%80_%E0%A4%B5%E0%A4%BE%E0%A4%9C%E0%A4%AA%E0%A5%87%E0%A4%AF%E0%A5%80"},
    {"title": "विश्व-नागरिक / बाजार में स्त्री", "poet": "वीरेंद्र गोयल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B5%E0%A4%BF%E0%A4%B6%E0%A5%8D%E0%A4%B5-%E0%A4%A8%E0%A4%BE%E0%A4%97%E0%A4%B0%E0%A4%BF%E0%A4%95_%2F_%E0%A4%AC%E0%A4%BE%E0%A4%9C%E0%A4%BE%E0%A4%B0_%E0%A4%AE%E0%A5%87%E0%A4%82_%E0%A4%B8%E0%A5%8D%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A5%80_%2F_%E0%A4%B5%E0%A5%80%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A4%A6%E0%A5%8D%E0%A4%B0_%E0%A4%97%E0%A5%8B%E0%A4%AF%E0%A4%B2"},
    {"title": "गोपन", "poet": "सुमित्रानंदन पंत", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%97%E0%A5%8B%E0%A4%AA%E0%A4%A8_%2F_%E0%A4%B8%E0%A5%81%E0%A4%AE%E0%A4%BF%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A8%E0%A4%82%E0%A4%A6%E0%A4%A8_%E0%A4%AA%E0%A4%82%E0%A4%A4"},
    {"title": "तोहफ़ो", "poet": "मुकेश तिलोकाणी", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%A4%E0%A5%8B%E0%A4%B9%E0%A4%AB%E0%A4%BC%E0%A5%8B_%2F_%E0%A4%AE%E0%A5%81%E0%A4%95%E0%A5%87%E0%A4%B6_%E0%A4%A4%E0%A4%BF%E0%A4%B2%E0%A5%8B%E0%A4%95%E0%A4%BE%E0%A4%A3%E0%A5%80"},
    {"title": "अक्लमंद बुद्धू", "poet": "लालित्य ललित", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%85%E0%A4%95%E0%A5%8D%E0%A4%B2%E0%A4%AE%E0%A4%82%E0%A4%A6_%E0%A4%AC%E0%A5%81%E0%A4%A6%E0%A5%8D%E0%A4%A7%E0%A5%82_%2F_%E0%A4%B2%E0%A4%BE%E0%A4%B2%E0%A4%BF%E0%A4%A4%E0%A5%8D%E0%A4%AF_%E0%A4%B2%E0%A4%B2%E0%A4%BF%E0%A4%A4"},
    {"title": "हत्यारों का घोषणापत्र", "poet": "मंगलेश डबराल", "url": "https://kavitakosh.org/kk/index.php?title=%E0%A4%B9%E0%A4%A4%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%B0%E0%A5%8B%E0%A4%82_%E0%A4%95%E0%A4%BE_%E0%A4%98%E0%A5%8B%E0%A4%B7%E0%A4%A3%E0%A4%BE%E0%A4%AA%E0%A4%A4%E0%A5%8D%E0%A4%B0_%2F_%E0%A4%AE%E0%A4%82%E0%A4%97%E0%A4%B2%E0%A5%87%E0%A4%B6_%E0%A4%A1%E0%A4%AC%E0%A4%B0%E0%A4%BE%E0%A4%B2"},
]
