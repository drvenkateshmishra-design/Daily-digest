"""Entry point: fetch content, build the PDF, email it. Run daily by GitHub Actions."""
import os
from fetch_news import fetch_news, fetch_blogs
from fetch_journals import fetch_journals
from build_pdf import build_pdf
from send_email import send as send_email

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "digest.pdf")


def main():
    print("Fetching news...")
    news, news_warnings = fetch_news()
    print("Fetching blogs...")
    blogs, blog_warnings = fetch_blogs()
    print("Fetching journal articles...")
    journals = fetch_journals()
    print("Building PDF...")
    build_pdf(news, journals, OUTPUT_PATH, blogs=blogs, feed_warnings=news_warnings + blog_warnings)
    print("Sending email...")
    send_email(OUTPUT_PATH)
    print("Done.")


if __name__ == "__main__":
    main()
