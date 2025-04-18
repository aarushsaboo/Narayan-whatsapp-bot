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
    print(phone_number)

    transactions  = await get_transactions_by_phone(phone_number)
    print(transactions)
    message_text  = format_transaction_email(transactions)

    # 2️⃣ Generate PDF bytes
    pdf_bytes = generate_pdf(transactions)

    print("ErROR? 2")

    # inside send_receipt_whatsapp, replace upload logic with:
    file_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"


    # 4️⃣ Send via Twilio (also in a thread)
    def _send():
        to_number = 'whatsapp:+919158898111'
        return client.messages.create(
            from_="whatsapp:+14155238886",
            to=to_number,
            body=message_text,
            media_url=[file_url]
        )

    sent = await asyncio.to_thread(_send)
    print("ErROR? 4")

    return {
        "to":    f"whatsapp:+{phone_number.lstrip('+')}",
        "sid":   sent.sid,
        "status": sent.status,
        "pdf_url": file_url
    }
