"""Entry point: fetch content, build the PDF, send it to Telegram. Run daily by GitHub Actions."""
import os

from fetch_news import fetch_news
from fetch_journals import fetch_journals
from build_pdf import build_pdf
from send_telegram import send as send_telegram

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "digest.pdf")


def main():
    print("Fetching news...")
    news = fetch_news()
    print("Fetching journal articles...")
    journals = fetch_journals()

    print("Building PDF...")
    build_pdf(news, journals, OUTPUT_PATH)

    print("Sending to Telegram...")
    send_telegram(OUTPUT_PATH)

    print("Done.")


if __name__ == "__main__":
    main()
