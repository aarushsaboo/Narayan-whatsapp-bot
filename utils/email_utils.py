import sendgrid
import os
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import asyncio
import asyncpg
from env import SENDGRID_API_KEY, NEON_DB_USER, NEON_DB_PASSWORD, NEON_DB_HOST, NEON_DB_PORT, NEON_DB_NAME
import base64
from utils.pdf_generator import generate_pdf

sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)

async def get_transactions_by_phone(phone_number):
    try:
        dsn = f"postgresql://{NEON_DB_USER}:{NEON_DB_PASSWORD}@{NEON_DB_HOST}:{NEON_DB_PORT}/{NEON_DB_NAME}"
        conn = await asyncpg.connect(dsn)

        try:
            query = """
                SELECT transaction_id, amount::text, transaction_date, payment_method, status
                FROM transactions
                WHERE phone_number = $1
                ORDER BY transaction_date DESC
            """
            rows = await conn.fetch(query, phone_number)

            # Optional: Convert amounts to float and rows to dicts
            transactions = []
            for row in rows:
                txn = dict(row)
                txn['amount'] = float(txn['amount'])
                transactions.append(txn)

            return transactions

        finally:
            await conn.close()

    except Exception as e:
        print(f"Error retrieving transactions: {e}")
        return []

def format_transaction_email(transactions):
    if not transactions:
        return "We couldn't find any transactions associated with your number."

    lines = ["Here are your recent transactions:\n"]
    for txn in transactions:
        lines.append(
            f"- ID: {txn['transaction_id']}, ₹{txn['amount']}, "
            f"{txn['transaction_date'].strftime('%Y-%m-%d')}, "
            f"{txn['payment_method']} ({txn['status']})"
        )
    return "\n".join(lines)

async def handle_email_receipt_request(query, sender_phone, client):
    transactions = await get_transactions_by_phone(sender_phone)
    email_body = format_transaction_email(transactions)

    from_email = Email("aarush.saboo@gmail.com")
    to_email = To("aarush.s@somaiya.edu")  # you can also fetch user email from DB if needed
    subject = "Your Transaction Receipt Summary"
    content = Content("text/plain", email_body)
    mail = Mail(from_email, to_email, subject, content)

    # Generate PDF
    pdf_data = generate_pdf(transactions)
    encoded_pdf = base64.b64encode(pdf_data).decode()

    attachment = Attachment()
    attachment.file_content = FileContent(encoded_pdf)
    attachment.file_type = FileType("application/pdf")
    attachment.file_name = FileName("receipt_summary.pdf")
    attachment.disposition = Disposition("attachment")
    mail.attachment = attachment

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(f"✅ Email sent: {response.status_code}")
        return "I’ve emailed you a summary of your transactions. Let me know if you need anything else!"
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return "I ran into an issue while sending your transaction receipt. Please try again later."
