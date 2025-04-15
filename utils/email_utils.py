import sendgrid
import os
from dotenv import load_dotenv
from sendgrid.helpers.mail import *
import asyncio

load_dotenv()

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

async def handle_email_receipt_request_async(query, sender_phone, client):
    from_email = Email("aarush.saboo@gmail.com")
    to_email = To("aarush.s@somaiya.edu")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def handle_email_receipt_request(query, sender_phone, client):
    return handle_email_receipt_request_async(query, sender_phone, client)
