"""Emails the generated PDF via Gmail SMTP. No app/account approval needed —
just a Gmail App Password (see README)."""
import os
import sys
import smtplib
from email.message import EmailMessage
from datetime import datetime


def send(pdf_path):
    gmail_address = os.environ["GMAIL_ADDRESS"]
    gmail_app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ.get("RECIPIENT_EMAIL", gmail_address)  # defaults to sending to yourself

    msg = EmailMessage()
    msg["Subject"] = f"Daily Digest — {datetime.now().strftime('%d %b %Y')}"
    msg["From"] = gmail_address
    msg["To"] = recipient
    msg.set_content("Your daily digest is attached.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(), maintype="application", subtype="pdf", filename="daily-digest.pdf"
        )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(gmail_address, gmail_app_password)
        server.send_message(msg)

    print(f"[send_email] Sent to {recipient}.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python send_email.py <path_to_pdf>")
        sys.exit(1)
    send(sys.argv[1])
