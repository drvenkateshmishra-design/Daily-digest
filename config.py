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
