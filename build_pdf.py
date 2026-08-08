"""Builds the formatted PDF from fetched news + journal data using reportlab."""
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

import config

NAVY = HexColor("#1a2b4c")
GREY = HexColor("#666666")
ACCENT = HexColor("#c0392b")


def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle("DocTitle", parent=ss["Title"], textColor=NAVY, fontSize=22, spaceAfter=2))
    ss.add(ParagraphStyle("DateLine", parent=ss["Normal"], textColor=GREY, fontSize=10, spaceAfter=14))
    ss.add(ParagraphStyle("SectionHeader", parent=ss["Heading1"], textColor=NAVY, fontSize=14,
                           spaceBefore=16, spaceAfter=6, borderPadding=0))
    ss.add(ParagraphStyle("SubHeader", parent=ss["Heading2"], textColor=ACCENT, fontSize=11.5,
                           spaceBefore=10, spaceAfter=4))
    ss.add(ParagraphStyle("Item", parent=ss["Normal"], fontSize=10, leading=14,
                           leftIndent=12, spaceBefore=5, bulletIndent=0))
    ss.add(ParagraphStyle("ItemMeta", parent=ss["Normal"], fontSize=8.5, textColor=GREY,
                           leading=11, leftIndent=22, spaceAfter=2))
    ss.add(ParagraphStyle("Empty", parent=ss["Normal"], fontSize=9.5, textColor=GREY,
                           spaceAfter=4, leftIndent=10))
    return ss


def build_pdf(news, journals, output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=18 * mm, bottomMargin=18 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
    )
    ss = _styles()
    story = []

    today_str = datetime.now().strftime("%A, %d %B %Y")
    story.append(Paragraph(config.PDF_TITLE, ss["DocTitle"]))
    story.append(Paragraph(today_str, ss["DateLine"]))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=10))

    # ---- NEWS ----
    story.append(Paragraph("NEWS", ss["SectionHeader"]))
    for section, items in news.items():
        story.append(Paragraph(section, ss["SubHeader"]))
        if not items:
            story.append(Paragraph("Nothing new in this section today.", ss["Empty"]))
            continue
        for it in items:
            text = f'\u2022 <link href="{it["link"]}" color="#1a2b4c">{it["title"]}</link>'
            story.append(Paragraph(text, ss["Item"]))
            story.append(Paragraph(it["source"], ss["ItemMeta"]))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceBefore=6, spaceAfter=10))

    # ---- JOURNALS ----
    story.append(Paragraph("JOURNAL WATCH", ss["SectionHeader"]))
    for section, items in journals.items():
        story.append(Paragraph(section, ss["SubHeader"]))
        if not items:
            story.append(Paragraph("No new articles matched this search in the lookback window.", ss["Empty"]))
            continue
        for it in items:
            mark = "\u2605 " if it["tier1"] else "\u2022 "  # star for tier-1 journals, bullet otherwise
            text = f'{mark}<link href="{it["link"]}" color="#1a2b4c">{it["title"]}</link>'
            story.append(Paragraph(text, ss["Item"]))
            meta = f'{it["journal"]} &middot; {it["pubdate"]}'
            story.append(Paragraph(meta, ss["ItemMeta"]))

    doc.build(story)
    return output_path


if __name__ == "__main__":
    # Quick smoke test with fake data
    news = {"Test Section": [{"title": "Sample headline", "link": "https://example.com", "source": "Example"}]}
    journals = {"Test Journals": [{"title": "Sample article", "journal": "Pediatrics", "pubdate": "2026 Aug", "link": "https://pubmed.ncbi.nlm.nih.gov/", "tier1": True}]}
    build_pdf(news, journals, "/tmp/test_digest.pdf")
    print("Built /tmp/test_digest.pdf")
