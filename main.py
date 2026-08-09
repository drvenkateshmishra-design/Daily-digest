"""Entry point: fetch content, build the PDF, email it. Run daily by GitHub Actions."""
import os
from fetch_news import fetch_news, fetch_blogs
from fetch_journals import fetch_journals
from build_pdf import build_pdf
from send_email import send as send_email
from seen_store import load_seen, save_seen, mark_seen, prune

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "digest.pdf")


def main():
    seen = load_seen()
    print(f"Loaded {len(seen)} previously-seen items")

    print("Fetching news...")
    news, news_warnings = fetch_news(already_seen_keys=set(seen.keys()))
    print("Fetching blogs...")
    blogs, blog_warnings = fetch_blogs(already_seen_keys=set(seen.keys()))
    print("Fetching journal articles...")
    journals = fetch_journals()
    print("Building PDF...")
    build_pdf(news, journals, OUTPUT_PATH, blogs=blogs,
              feed_warnings=news_warnings + blog_warnings)

    # Record today's items so tomorrow's run doesn't repeat them, then prune
    # anything old enough it'll never recur anyway. Saved before send_email()
    # runs — if delivery fails, we still want tomorrow's run to reflect what
    # was actually built today, not retry from stale state.
    mark_seen(seen, news)
    mark_seen(seen, blogs)
    seen = prune(seen)
    save_seen(seen)
    print(f"Saved {len(seen)} seen items for next run")

    print("Sending email...")
    send_email(OUTPUT_PATH)
    print("Done.")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
