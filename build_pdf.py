"""Builds the formatted PDF from fetched news + journal data using reportlab.

Newspaper-styled: serif (Times) typography throughout, a broadsheet-style
masthead (nameplate + motto + edition/date line, double rules), and each
news item rendered as headline + excerpt + byline + explicit "read full
article" link.
"""
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
import config

NAVY = HexColor("#1a2b4c")
GREY = HexColor("#666666")
LIGHT_RULE = HexColor("#bbbbbb")
ACCENT = HexColor("#c0392b")
INK = HexColor("#1a1a1a")
BLACK = HexColor("#000000")


def _styles():
    ss = getSampleStyleSheet()

    # ---- Masthead (broadsheet-style nameplate) ----
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

    # ---- Section / sub-section headers ----
    ss.add(ParagraphStyle("SectionHeader", parent=ss["Heading1"], fontName="Times-Bold",
                           textColor=NAVY, fontSize=15, leading=18,
                           spaceBefore=18, spaceAfter=4, tracking=1))
    ss.add(ParagraphStyle("SubHeader", parent=ss["Heading2"], fontName="Times-BoldItalic",
                           textColor=ACCENT, fontSize=12, leading=15,
                           spaceBefore=12, spaceAfter=6))

    # ---- Story blocks ----
    ss.add(ParagraphStyle("Headline", parent=ss["Normal"], fontName="Times-Bold",
                           fontSize=11.5, leading=14.5, textColor=INK,
                           spaceBefore=7, spaceAfter=2))
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
    return ss


def _byline(it):
    """'Source Name · 08 August 2026' — falls back gracefully if no date."""
    source = it.get("source", "")
    published = it.get("published")
    if published:
        return f'{source} &middot; {published.strftime("%d %B %Y")}'
    return source


def _story_block(it, ss, story, headline_text, meta_text):
    story.append(Paragraph(headline_text, ss["Headline"]))
    if it.get("excerpt"):
        story.append(Paragraph(it["excerpt"], ss["Excerpt"]))
    story.append(Paragraph(meta_text, ss["Byline"]))
    link = it.get("link")
    if link:
        story.append(Paragraph(
            f'<link href="{link}" color="#c0392b">Read full article &#187;</link>',
            ss["ReadMore"]
        ))


def build_pdf(news, journals, output_path):
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
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(edition_row)
    story.append(HRFlowable(width="100%", thickness=3, color=BLACK, spaceBefore=3, spaceAfter=2))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BLACK, spaceBefore=1, spaceAfter=16))

    # ---- NEWS ----
    story.append(Paragraph("NEWS", ss["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=8))

    for section, items in news.items():
        story.append(Paragraph(section.upper(), ss["SubHeader"]))
        if not items:
            story.append(Paragraph("Nothing new in this section today.", ss["Empty"]))
            continue
        for i, it in enumerate(items):
            headline = f'<link href="{it["link"]}" color="#1a2b4c">{it["title"]}</link>' if it.get("link") else it["title"]
            _story_block(it, ss, story, headline, _byline(it))
            if i < len(items) - 1:
                story.append(HRFlowable(width="35%", thickness=0.4, color=LIGHT_RULE,
                                         spaceBefore=4, spaceAfter=2, hAlign="LEFT"))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2.2, color=NAVY, spaceBefore=4, spaceAfter=2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceBefore=1, spaceAfter=14))

    # ---- JOURNALS ----
    story.append(Paragraph("JOURNAL WATCH", ss["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=8))

    for section, items in journals.items():
        story.append(Paragraph(section.upper(), ss["SubHeader"]))
        if not items:
            story.append(Paragraph("No new articles matched this search in the lookback window.", ss["Empty"]))
            continue
        for i, it in enumerate(items):
            mark = "&#9733; " if it["tier1"] else ""  # star prefix for tier-1 journals
            headline = f'{mark}<link href="{it["link"]}" color="#1a2b4c">{it["title"]}</link>' if it.get("link") else f'{mark}{it["title"]}'
            meta = f'{it["journal"]} &middot; {it["pubdate"]}'
            _story_block(it, ss, story, headline, meta)
            if i < len(items) - 1:
                story.append(HRFlowable(width="35%", thickness=0.4, color=LIGHT_RULE,
                                         spaceBefore=4, spaceAfter=2, hAlign="LEFT"))

    doc.build(story)
    return output_path


if __name__ == "__main__":
    # Quick smoke test with fake data
    news = {
        "Test Section": [
            {
                "title": "Sample headline goes here",
                "link": "https://example.com",
                "source": "Example Times",
                "published": datetime.now(),
                "excerpt": "This is a sample excerpt pulled from the feed's own summary "
                           "field, long enough to show how the justified body text wraps "
                           "across a couple of lines in the newspaper-style layout.",
            }
        ]
    }
    journals = {
        "Test Journals": [
            {"title": "Sample article", "journal": "Pediatrics", "pubdate": "2026 Aug",
             "link": "https://pubmed.ncbi.nlm.nih.gov/", "tier1": True}
        ]
    }
    build_pdf(news, journals, "/tmp/test_digest2.pdf")
    print("Built /tmp/test_digest2.pdf")
