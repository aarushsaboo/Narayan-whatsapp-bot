# Main application file
import os
import asyncio
from dotenv import load_dotenv
from twilio.rest import Client
from flask import jsonify

from utils.email_utils import get_transactions_by_phone, format_transaction_email
from utils.pdf_generator import generate_pdf
from utils.supabase_utils import upload_pdf_to_supabase

# ── Twilio setup ───────────────────────────────────────────────────────────────
load_dotenv()
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
client = Client(ACCOUNT_SID, AUTH_TOKEN)

async def send_receipt_whatsapp(name, phone_number, amount):
    try:
        # 1️⃣ Fetch & format
        print(f"Processing receipt for {phone_number}")
        
        transactions = await get_transactions_by_phone(phone_number)
        print(f"Found {len(transactions)} transactions")
        message_text = format_transaction_email(transactions)
        
        # 2️⃣ Generate PDF bytes
        pdf_bytes = generate_pdf(transactions)
        print("PDF generated successfully")
        
        # 3️⃣ Upload to Supabase and get URL
        media_url = await upload_pdf_to_supabase(pdf_bytes, phone_number)
        print(f"PDF uploaded, URL: {media_url}")
        
        
        body = "Here's your payment receipt! 🧾"

        formatted_number = "whatsapp:" + phone_number
        message = client.messages.create(
            body=body,
            from_="whatsapp:+14155238886",
            to=formatted_number,
            media_url=[media_url]
        )
        
        return jsonify({"message_sid": message.sid, "status": "sent!"})
        
        # return {
        #     "to": f"whatsapp:+{phone_number.lstrip('+')}",
        #     "sid": sent.sid,
        #     "status": sent.status,
        #     "pdf_url": file_url
        # }
    except Exception as e:
        print(f"Error in send_receipt_whatsapp: {str(e)}")
        # Return error information for debugging
        return {
            "error": str(e),
            "status": "failed",
            "to": f"whatsapp:+{phone_number.lstrip('+')}" if phone_number else "unknown"
        }