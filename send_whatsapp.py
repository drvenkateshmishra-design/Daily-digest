"""Sends the generated PDF over WhatsApp via Twilio, once its public URL is live."""
import os
import sys
import time
import requests
from twilio.rest import Client

import config


def wait_until_live(url, timeout_seconds=180, interval_seconds=8):
    """GitHub Pages takes a little time to publish after a push. Poll until the
    PDF URL actually responds before handing it to Twilio, so Twilio doesn't
    fetch a 404."""
    waited = 0
    while waited < timeout_seconds:
        try:
            r = requests.head(url, timeout=10, allow_redirects=True)
            if r.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(interval_seconds)
        waited += interval_seconds
    return False


def send(pdf_public_url):
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    to_number = os.environ["TWILIO_WHATSAPP_TO"]  # e.g. "whatsapp:+9198XXXXXXXX"

    if not wait_until_live(pdf_public_url):
        print(f"[send_whatsapp] WARNING: {pdf_public_url} never returned 200 within timeout. "
              f"Attempting send anyway.")

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=config.TWILIO_WHATSAPP_FROM,
        to=to_number,
        body="Your daily digest is ready.",
        media_url=[pdf_public_url],
    )
    print(f"[send_whatsapp] Sent. SID: {message.sid}, status: {message.status}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python send_whatsapp.py <public_pdf_url>")
        sys.exit(1)
    send(sys.argv[1])
