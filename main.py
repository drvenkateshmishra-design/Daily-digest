"""Entry point: fetch content, build the PDF, save it into docs/ for GitHub Pages."""
import os
from datetime import datetime

from fetch_news import fetch_news
from fetch_journals import fetch_journals
from build_pdf import build_pdf

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "docs")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Fetching news...")
    news = fetch_news()
    print("Fetching journal articles...")
    journals = fetch_journals()

    date_str = datetime.now().strftime("%Y-%m-%d")
    dated_path = os.path.join(OUTPUT_DIR, f"digest-{date_str}.pdf")
    latest_path = os.path.join(OUTPUT_DIR, "latest.pdf")

    print("Building PDF...")
    build_pdf(news, journals, dated_path)
    build_pdf(news, journals, latest_path)  # same content, stable filename for WhatsApp

    print(f"Done. Wrote {dated_path} and {latest_path}")


if __name__ == "__main__":
    main()
