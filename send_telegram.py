"""Sends the generated PDF to your Telegram chat via a bot. Free, no hosting needed —
the file is uploaded directly to Telegram's API."""
import os
import sys
import requests


def send(pdf_path):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(pdf_path, "rb") as f:
        resp = requests.post(
            url,
            data={"chat_id": chat_id, "caption": "Your daily digest is ready."},
            files={"document": ("daily-digest.pdf", f, "application/pdf")},
            timeout=60,
        )

    if resp.status_code != 200:
        print(f"[send_telegram] FAILED: {resp.status_code} {resp.text}")
        resp.raise_for_status()

    print(f"[send_telegram] Sent successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python send_telegram.py <path_to_pdf>")
        sys.exit(1)
    send(sys.argv[1])
