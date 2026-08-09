"""Builds the formatted PDF from fetched news + journal data using reportlab.

Newspaper-styled: serif (Times) typography, a broadsheet masthead, a front
page of teasers, real images from the RSS feeds where available (two-column
image+text layout per story), colored section "kicker" tags, and a quiet
feed-health footer when something's broken.
"""
from datetime import datetime, date
import os
import random
from io import BytesIO
import requests
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
                                 Table, TableStyle, Image, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import config

# Devanagari needs its own embedded font — the standard PDF fonts (Times etc.)
# have no Devanagari glyphs at all. Falls back gracefully (Latin
# transliteration only, no boxes/garbage) if the font file isn't present.
DEVANAGARI_FONT = "NotoDevanagari"
_FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "NotoSerifDevanagari.ttf")
try:
    pdfmetrics.registerFont(TTFont(DEVANAGARI_FONT, _FONT_PATH))
    DEVANAGARI_AVAILABLE = True
except Exception as e:
    print(f"[pdf] Devanagari font not available ({e}) — Sanskrit/Hindi will show transliteration only")
    DEVANAGARI_AVAILABLE = False

NAVY = HexColor("#1a2b4c")
GREY = HexColor("#666666")
LIGHT_RULE = HexColor("#bbbbbb")
ACCENT = HexColor("#c0392b")
INK = HexColor("#1a1a1a")
BLACK = HexColor("#000000")

CONTENT_WIDTH = 170 * mm  # A4 width minus 20mm margins each side
IMG_COL_WIDTH = 38 * mm
IMG_MAX_HEIGHT = 30 * mm
TEXT_COL_WIDTH = CONTENT_WIDTH - IMG_COL_WIDTH - 4 * mm
TEASER_IMG_WIDTH = 26 * mm
TEASER_IMG_HEIGHT = 19 * mm


def _styles():
    ss = getSampleStyleSheet()

    ss.add(ParagraphStyle("Nameplate", parent=ss["Title"], fontName="Times-Bold",
                           textColor=BLACK, fontSize=40, leading=42,
                           alignment=TA_CENTER, spaceAfter=1))
    ss.add(ParagraphStyle("Motto", parent=ss["Normal"], fontName="Times-Italic",
                           textColor=GREY, fontSize=9, alignment=TA_CENTER,
                           spaceAfter=4))
    ss.add(ParagraphStyle("EditionLeft", parent=ss["Normal"], fontName="Times-Bold",
                           textColor=INK, fontSize=8.5, alignment=TA_LEFT))
    ss.add(ParagraphStyle("EditionRight", parent=ss["Normal"], fontName="Times-Roman",
                           textColor=INK, fontSize=8.5, alignment=TA_RIGHT))

    ss.add(ParagraphStyle("SectionHeader", parent=ss["Heading1"], fontName="Times-Bold",
                           textColor=NAVY, fontSize=15, leading=18,
                           spaceBefore=18, spaceAfter=4, tracking=1))
    ss.add(ParagraphStyle("Kicker", parent=ss["Normal"], fontName="Times-Bold",
                           textColor=white, fontSize=8.5, leading=11,
                           alignment=TA_LEFT))

    ss.add(ParagraphStyle("Headline", parent=ss["Normal"], fontName="Times-Bold",
                           fontSize=11.5, leading=14.5, textColor=INK,
                           spaceBefore=0, spaceAfter=2))
    ss.add(ParagraphStyle("Excerpt", parent=ss["Normal"], fontName="Times-Roman",
                           fontSize=9.7, leading=13, textColor=INK,
                           alignment=TA_JUSTIFY, spaceAfter=3))
    ss.add(ParagraphStyle("Byline", parent=ss["Normal"], fontName="Times-Italic",
                           fontSize=8.3, leading=10.5, textColor=GREY,
                           spaceAfter=1))
    ss.add(ParagraphStyle("ReadMore", parent=ss["Normal"], fontName="Times-Italic",
                           fontSize=8.3, leading=10.5, textColor=ACCENT,
                           spaceAfter=1))
    ss.add(ParagraphStyle("Empty", parent=ss["Normal"], fontName="Times-Italic",
                           fontSize=9.5, textColor=GREY, spaceAfter=4))

    ss.add(ParagraphStyle("TeaserLabel", parent=ss["Normal"], fontName="Times-Bold",
                           fontSize=8, textColor=ACCENT, spaceAfter=1))
    ss.add(ParagraphStyle("TeaserHeadline", parent=ss["Normal"], fontName="Times-Bold",
                           fontSize=10.5, leading=13, textColor=INK, spaceAfter=1))
    ss.add(ParagraphStyle("TeaserDek", parent=ss["Normal"], fontName="Times-Roman",
                           fontSize=9, leading=11.5, textColor=INK, spaceAfter=2))

    ss.add(ParagraphStyle("MaintHeader", parent=ss["Normal"], fontName="Times-Bold",
                           fontSize=9, textColor=GREY, spaceBefore=4, spaceAfter=3))
    ss.add(ParagraphStyle("MaintItem", parent=ss["Normal"], fontName="Times-Roman",
                           fontSize=7.8, leading=10, textColor=GREY, spaceAfter=1))

    # ---- Thoughts for the day (Sanskrit / English / Hindi) ----
    deva_font = DEVANAGARI_FONT if DEVANAGARI_AVAILABLE else "Times-Roman"
    ss.add(ParagraphStyle("ThoughtsHeader", parent=ss["Normal"], fontName="Times-BoldItalic",
                           fontSize=9.5, textColor=white, alignment=TA_CENTER, spaceAfter=0))
    ss.add(ParagraphStyle("DevaQuote", parent=ss["Normal"], fontName=deva_font,
                           fontSize=13, leading=24, textColor=INK, alignment=TA_CENTER, spaceAfter=2))
    ss.add(ParagraphStyle("DevaMeta", parent=ss["Normal"], fontName="Times-Italic",
                           fontSize=8.3, leading=11, textColor=GREY, alignment=TA_CENTER, spaceAfter=0))
    ss.add(ParagraphStyle("EnglishQuote", parent=ss["Normal"], fontName="Times-Italic",
                           fontSize=10.5, leading=14, textColor=INK, alignment=TA_CENTER, spaceAfter=2))
    ss.add(ParagraphStyle("EnglishMeta", parent=ss["Normal"], fontName="Times-Roman",
                           fontSize=8.3, leading=11, textColor=GREY, alignment=TA_CENTER, spaceAfter=0))
    ss.add(ParagraphStyle("DevaPoem", parent=ss["Normal"], fontName=deva_font,
                           fontSize=11.5, leading=21, textColor=INK, alignment=TA_CENTER, spaceAfter=2))
    ss.add(ParagraphStyle("DevaPoetMeta", parent=ss["Normal"], fontName=deva_font,
                           fontSize=8.3, leading=14, textColor=GREY, alignment=TA_CENTER, spaceAfter=0))
    # ---- Ek Kavita Roj (daily poem link — title/poet only, links out; see
    # _ek_kavita_roj()) — reuses DevaPoem/DevaPoetMeta above, plus this one
    # extra style for the outbound link itself, which needs the Devanagari
    # font (unlike ReadMore above, which is only ever used on ASCII text).
    ss.add(ParagraphStyle("DevaReadMore", parent=ss["Normal"], fontName=deva_font,
                           fontSize=8.5, leading=13, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=0))
    ss.add(ParagraphStyle("KavitaHeader", parent=ss["Normal"], fontName=deva_font,
                           fontSize=9.5, textColor=white, alignment=TA_CENTER, spaceAfter=0))
    return ss


# ---------------------------------------------------------------- images ---

_image_bytes_cache = {}


def _fetch_image_bytes(url, timeout=8):
    """Downloads raw image bytes once per URL per run. Returns None on any
    failure (timeout, non-image content-type, oversized, blocked, corrupt) —
    a missing image should never break the PDF, just fall back to text-only."""
    if not url:
        return None
    if url in _image_bytes_cache:
        return _image_bytes_cache[url]
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        if not r.headers.get("Content-Type", "").startswith("image"):
            _image_bytes_cache[url] = None
            return None
        data = r.content
        if len(data) > 4_000_000:  # 4MB safety cap
            _image_bytes_cache[url] = None
            return None
        _image_bytes_cache[url] = data
        return data
    except Exception as e:
        print(f"[pdf] Skipping image {url}: {e}")
        _image_bytes_cache[url] = None
        return None


def _make_image_flowable(url, max_w, max_h):
    """Fresh Image flowable each call (reportlab Image objects carry layout
    state, so never reuse one instance twice even if the bytes are cached)."""
    data = _fetch_image_bytes(url)
    if not data:
        return None
    try:
        pil_img = PILImage.open(BytesIO(data))
        orig_w, orig_h = pil_img.size
        if orig_w <= 0 or orig_h <= 0:
            return None
        scale = min(max_w / orig_w, max_h / orig_h, 1.0)  # never upscale
        return Image(BytesIO(data), width=orig_w * scale, height=orig_h * scale)
    except Exception as e:
        print(f"[pdf] Skipping malformed image {url}: {e}")
        return None


# ------------------------------------------------------------- kickers -----

def _kicker(text, ss):
    """A small colored 'flag' tag for a section label — hugs its own text
    width rather than spanning the page, like a magazine section tag."""
    t = Table([[Paragraph(text.upper(), ss["Kicker"])]], colWidths=None)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    t.hAlign = "LEFT"
    return t


def _thoughts_for_the_day(ss):
    """A bordered box with one Sanskrit shloka, one English quote, and one
    Hindi doha — all classical/public-domain, picked deterministically per
    calendar day (same picks if the workflow reruns same-day)."""
    rng = random.Random(int(date.today().strftime("%Y%m%d")))
    sk = rng.choice(config.SANSKRIT_QUOTES)
    en = rng.choice(config.ENGLISH_QUOTES)
    hi = rng.choice(config.HINDI_POEMS)

    inner = [
        Paragraph(sk["deva"], ss["DevaQuote"]),
        Paragraph(f'{sk["translit"]} — &ldquo;{sk["meaning"]}&rdquo; ({sk["source"]})', ss["DevaMeta"]),
        Spacer(1, 8),
        Paragraph(f'&ldquo;{en["text"]}&rdquo;', ss["EnglishQuote"]),
        Paragraph(f'— {en["author"]}', ss["EnglishMeta"]),
        Spacer(1, 8),
        Paragraph(hi["lines"], ss["DevaPoem"]),
        Paragraph(f'— {hi["poet"]}', ss["DevaPoetMeta"]),
    ]

    header = Table([[Paragraph("THOUGHTS FOR THE DAY", ss["ThoughtsHeader"])]], colWidths=[CONTENT_WIDTH])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    body = Table([[inner]], colWidths=[CONTENT_WIDTH])
    body.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, LIGHT_RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))

    return [header, body]


def _ek_kavita_roj(poem, ss):
    """Small bordered box linking to one random poem on Kavita Kosh — title
    and poet name only, NOT the poem text itself (Kavita Kosh hosts both
    public-domain and living/copyrighted poets with no reliable way to tell
    them apart automatically, so unlike Thoughts-for-the-Day this never
    reproduces the work — same 'Read full article »' link pattern used for
    every news/blog story elsewhere in this PDF). `poem` is the dict
    returned by fetch_kavita.fetch_kavita_roj() — title/poet/url — or None
    if that fetch failed, in which case the caller skips this box entirely."""
    inner = [
        Paragraph(poem["title"], ss["DevaPoem"]),
        Paragraph(f'— {poem["poet"]}', ss["DevaPoetMeta"]),
        Spacer(1, 4),
        Paragraph(f'<link href="{poem["url"]}" color="#c0392b">पूरी कविता पढ़ें (Kavita Kosh पर) &#187;</link>',
                   ss["DevaReadMore"]),
    ]

    header = Table([[Paragraph("एक कविता रोज़ · POEM OF THE DAY", ss["KavitaHeader"])]], colWidths=[CONTENT_WIDTH])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    body = Table([[inner]], colWidths=[CONTENT_WIDTH])
    body.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, LIGHT_RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))

    return [header, body]


# --------------------------------------------------------- story blocks ---

def _story_flowables(it, ss, headline_text, meta_text):
    flows = [Paragraph(headline_text, ss["Headline"])]
    body_text = it.get("excerpt") or it.get("abstract")
    if body_text:
        flows.append(Paragraph(body_text, ss["Excerpt"]))
    flows.append(Paragraph(meta_text, ss["Byline"]))
    link = it.get("link")
    if link:
        flows.append(Paragraph(
            f'<link href="{link}" color="#c0392b">Read full article &#187;</link>',
            ss["ReadMore"]
        ))
    return flows


def _story_block(it, ss, story, headline_text, meta_text, image_url=None):
    text_flows = _story_flowables(it, ss, headline_text, meta_text)
    img = _make_image_flowable(image_url, IMG_COL_WIDTH, IMG_MAX_HEIGHT) if image_url else None
    if img is not None:
        table = Table([[img, text_flows]], colWidths=[IMG_COL_WIDTH, TEXT_COL_WIDTH])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (0, 0), 0),
            ("RIGHTPADDING", (0, 0), (0, 0), 4 * mm),
            ("LEFTPADDING", (1, 0), (1, 0), 0),
            ("RIGHTPADDING", (1, 0), (1, 0), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(table)
    else:
        story.extend(text_flows)


def _byline(it):
    source = it.get("source", "")
    published = it.get("published")
    if published:
        return f'{source} &middot; {published.strftime("%d %B %Y")}'
    return source


def _teaser_dek(excerpt, max_chars=140):
    if not excerpt:
        return ""
    if len(excerpt) <= max_chars:
        return excerpt
    return excerpt[:max_chars].rsplit(" ", 1)[0].rstrip(".,;: ") + "…"


def _teaser_flowables(section, top, ss):
    flows = [Paragraph(section.upper(), ss["TeaserLabel"])]
    headline = (f'<link href="{top["link"]}" color="#1a2b4c">{top["title"]}</link>'
                if top.get("link") else top["title"])
    flows.append(Paragraph(headline, ss["TeaserHeadline"]))
    dek = _teaser_dek(top.get("excerpt", ""))
    if dek:
        flows.append(Paragraph(dek, ss["TeaserDek"]))
    return flows


def _teaser_block(section, top, ss, story):
    text_flows = _teaser_flowables(section, top, ss)
    img = _make_image_flowable(top.get("image"), TEASER_IMG_WIDTH, TEASER_IMG_HEIGHT) if top.get("image") else None
    if img is not None:
        text_col_w = CONTENT_WIDTH - TEASER_IMG_WIDTH - 4 * mm
        table = Table([[img, text_flows]], colWidths=[TEASER_IMG_WIDTH, text_col_w])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (0, 0), 0),
            ("RIGHTPADDING", (0, 0), (0, 0), 4 * mm),
            ("LEFTPADDING", (1, 0), (1, 0), 0),
            ("RIGHTPADDING", (1, 0), (1, 0), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(table)
    else:
        story.extend(text_flows)
        story.append(Spacer(1, 3))


# ------------------------------------------------------------- builder ----

def build_pdf(news, journals, output_path, blogs=None, feed_warnings=None, kavita_roj=None):
    blogs = blogs or {}
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=14 * mm, bottomMargin=18 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
    )
    ss = _styles()
    story = []

    today_str = datetime.now().strftime("%A, %d %B %Y")

    # ---- MASTHEAD ----
    story.append(HRFlowable(width="100%", thickness=3, color=BLACK, spaceAfter=5))
    story.append(Paragraph(config.PDF_TITLE.upper(), ss["Nameplate"]))
    story.append(Paragraph("&ldquo;News, Journals &amp; Everything Worth Knowing&rdquo;", ss["Motto"]))
    story.append(HRFlowable(width="100%", thickness=1.4, color=BLACK, spaceBefore=2, spaceAfter=3))

    edition_row = Table(
        [[Paragraph("DAILY EDITION", ss["EditionLeft"]),
          Paragraph(today_str, ss["EditionRight"])]],
        colWidths=[doc.width / 2.0, doc.width / 2.0],
    )
    edition_row.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(edition_row)
    story.append(HRFlowable(width="100%", thickness=3, color=BLACK, spaceBefore=3, spaceAfter=2))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BLACK, spaceBefore=1, spaceAfter=14))

    # ---- THOUGHTS FOR THE DAY ----
    story.extend(_thoughts_for_the_day(ss))
    story.append(Spacer(1, 12))

    # ---- EK KAVITA ROJ (daily poem link) — skipped entirely if the fetch
    # failed today (dead network, Kavita Kosh down, etc.); never blocks the build.
    if kavita_roj:
        story.extend(_ek_kavita_roj(kavita_roj, ss))
    story.append(Spacer(1, 16))

    # ---- FRONT PAGE ----
    story.append(Paragraph("TODAY'S HEADLINES", ss["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=8))

    any_teaser = False
    for section, items in news.items():
        if not items:
            continue
        any_teaser = True
        _teaser_block(section, items[0], ss, story)

    top_journal = None
    for section, items in journals.items():
        for it in items:
            if it.get("tier1"):
                top_journal = it
                break
        if top_journal:
            break
    if top_journal:
        story.append(Paragraph("ALSO INSIDE", ss["TeaserLabel"]))
        story.append(Paragraph(
            f'&#9733; Journal Watch — <link href="{top_journal["link"]}" color="#1a2b4c">{top_journal["title"]}</link>',
            ss["TeaserDek"]
        ))
        any_teaser = True

    if not any_teaser:
        story.append(Paragraph("No stories today.", ss["Empty"]))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2.2, color=NAVY, spaceBefore=2, spaceAfter=2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceBefore=1, spaceAfter=16))

    # ---- NEWS ----
    story.append(PageBreak())
    story.append(Paragraph("NEWS", ss["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=10))

    for section, items in news.items():
        story.append(_kicker(section, ss))
        story.append(Spacer(1, 6))
        if not items:
            story.append(Paragraph("Nothing new in this section today.", ss["Empty"]))
            story.append(Spacer(1, 10))
            continue
        for i, it in enumerate(items):
            headline = (f'<link href="{it["link"]}" color="#1a2b4c">{it["title"]}</link>'
                        if it.get("link") else it["title"])
            _story_block(it, ss, story, headline, _byline(it), image_url=it.get("image"))
            if i < len(items) - 1:
                story.append(HRFlowable(width="35%", thickness=0.4, color=LIGHT_RULE,
                                         spaceBefore=6, spaceAfter=6, hAlign="LEFT"))
            else:
                story.append(Spacer(1, 12))

    story.append(HRFlowable(width="100%", thickness=2.2, color=NAVY, spaceBefore=2, spaceAfter=2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceBefore=1, spaceAfter=14))

    # ---- BLOGS (long-form — these feeds carry full post text, not just a teaser) ----
    if blogs:
        story.append(PageBreak())
        story.append(Paragraph("BLOGS", ss["SectionHeader"]))
        story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=10))

        for section, items in blogs.items():
            story.append(_kicker(section, ss))
            story.append(Spacer(1, 6))
            if not items:
                story.append(Paragraph("No new posts in this section this week.", ss["Empty"]))
                story.append(Spacer(1, 10))
                continue
            for i, it in enumerate(items):
                headline = (f'<link href="{it["link"]}" color="#1a2b4c">{it["title"]}</link>'
                            if it.get("link") else it["title"])
                _story_block(it, ss, story, headline, _byline(it), image_url=it.get("image"))
                if i < len(items) - 1:
                    story.append(HRFlowable(width="35%", thickness=0.4, color=LIGHT_RULE,
                                             spaceBefore=6, spaceAfter=6, hAlign="LEFT"))
                else:
                    story.append(Spacer(1, 12))

        story.append(HRFlowable(width="100%", thickness=2.2, color=NAVY, spaceBefore=2, spaceAfter=2))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceBefore=1, spaceAfter=14))

    # ---- JOURNALS ----
    story.append(PageBreak())
    story.append(Paragraph("JOURNAL WATCH", ss["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=10))

    for section, items in journals.items():
        story.append(_kicker(section, ss))
        story.append(Spacer(1, 6))
        if not items:
            story.append(Paragraph("No new articles matched this search in the lookback window.", ss["Empty"]))
            story.append(Spacer(1, 10))
            continue
        for i, it in enumerate(items):
            mark = "&#9733; " if it["tier1"] else ""
            headline = (f'{mark}<link href="{it["link"]}" color="#1a2b4c">{it["title"]}</link>'
                        if it.get("link") else f'{mark}{it["title"]}')
            meta = f'{it["journal"]} &middot; {it["pubdate"]}'
            _story_block(it, ss, story, headline, meta)  # no images for PubMed articles
            if i < len(items) - 1:
                story.append(HRFlowable(width="35%", thickness=0.4, color=LIGHT_RULE,
                                         spaceBefore=6, spaceAfter=6, hAlign="LEFT"))
            else:
                story.append(Spacer(1, 12))

    # ---- MAINTENANCE FOOTER ----
    if feed_warnings:
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_RULE, spaceAfter=4))
        story.append(Paragraph(f"SOURCES NEEDING ATTENTION TODAY ({len(feed_warnings)})", ss["MaintHeader"]))
        for w in feed_warnings:
            story.append(Paragraph(w, ss["MaintItem"]))

    doc.build(story)
    return output_path


if __name__ == "__main__":
    news = {
        "Test Section": [
            {
                "title": "Sample headline goes here",
                "link": "https://example.com",
                "source": "Example Times",
                "published": datetime.now(),
                "excerpt": "This is a sample excerpt long enough to show how the "
                           "justified body text wraps in the newspaper-style layout.",
                "image": None,
            }
        ]
    }
    journals = {
        "Test Journals": [
            {"title": "Sample article", "journal": "Pediatrics", "pubdate": "2026 Aug",
             "link": "https://pubmed.ncbi.nlm.nih.gov/", "tier1": True}
        ]
    }
    build_pdf(news, journals, "/tmp/test_digest3.pdf")
    print("Built /tmp/test_digest3.pdf")
