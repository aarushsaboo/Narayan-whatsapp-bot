import os
import asyncio
import requests
from dotenv import load_dotenv
from twilio.rest import Client

from utils.email_utils import get_transactions_by_phone, format_transaction_email
from utils.pdf_generator import generate_pdf

# ── Twilio setup ───────────────────────────────────────────────────────────────
load_dotenv()
ACCOUNT_SID       = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN        = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM     = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
client            = Client(ACCOUNT_SID, AUTH_TOKEN)

async def send_receipt_whatsapp(name, phone_number, amount):
    # 1️⃣ Fetch & format
    transactions  = await get_transactions_by_phone(phone_number)
    message_text  = format_transaction_email(transactions)

    # 2️⃣ Generate PDF bytes
    pdf_bytes = generate_pdf(transactions)

    # 3️⃣ Upload PDF to file.io (in a thread to avoid blocking)
    def _upload():
        resp = requests.post(
            "https://file.io",
            files={"file": ("receipt.pdf", pdf_bytes, "application/pdf")}
        )
        resp.raise_for_status()
        return resp.json()["link"]

    file_url = await asyncio.to_thread(_upload)

    # 4️⃣ Send via Twilio (also in a thread)
    def _send():
        return client.messages.create(
            from_=WHATSAPP_FROM,
            to=f"whatsapp:+{phone_number.lstrip('+')}",
            body=message_text,
            media_url=[file_url]
        )

    sent = await asyncio.to_thread(_send)

    return {
        "to":    f"whatsapp:+{phone_number.lstrip('+')}",
        "sid":   sent.sid,
        "status": sent.status,
        "pdf_url": file_url
    }
