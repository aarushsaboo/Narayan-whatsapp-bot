# app.py
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from google import genai
from env import GEMINI_API_KEY
from response_generator import generate_response
from flask_cors import CORS
from donations.insert_in_db import insert_in_db
from donations.send_receipt_whatsapp import send_receipt_whatsapp
from utils.email_utils import handle_email_receipt_request
import asyncio

app = Flask(__name__)
CORS(app) 

# Initialize Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY,
)

@app.route('/twilio_webhook', methods=['POST'])
def twilio_webhook():
    print("Raw Twilio Request Data:")
    print(request.form)

    sender_phone = request.form.get('From')
    message_body = request.form.get('Body')

    print(f"Phone number from request: {sender_phone}")
    print(f"Message body from request: {message_body}")

    if not sender_phone or not message_body:
        error_message = "<Response><Message>Error: Phone number and message are required.</Message></Response>"
        return error_message, 400, {'Content-Type': 'application/xml'}

    if sender_phone.startswith('whatsapp:'):
        sender_phone = sender_phone.replace('whatsapp:', '')

    response_text = generate_response(message_body, sender_phone, client)

    response = MessagingResponse()
    response.message(response_text)

    twiml_string = str(response)

    return twiml_string, 200, {'Content-Type': 'application/xml'}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "WhatsApp backend is healthy"}), 200

@app.route('/', methods=['GET', 'HEAD'])
def root():
    return jsonify({"status": "ok", "message": "Narayan Shiva Sansthan WhatsApp Service"}), 200

@app.route('/payment', methods=['POST'])
# the kind of data it is receiving: {
#     name: name,
#     phoneNumber: phone,
#     amount: parseFloat(amount),
#   }
def payment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    name        = data.get("name")
    phone       = data.get("phoneNumber")
    amount      = data.get("amount")

    asyncio.run(insert_in_db(data.get("name"), data.get("phoneNumber"), data.get("amount")))

    response_text = "We're sending you the receipt for your records. Thanks for your support!"
    
    print("what is going on 1?")
    whatsapp_res = asyncio.run(send_receipt_whatsapp(name, phone, amount))

    asyncio.run(handle_email_receipt_request("", data.get("phoneNumber"), client))

    
    response = MessagingResponse()
    response.message(response_text)

    twiml_string = str(response)

    return twiml_string, 200, {'Content-Type': 'application/xml'}
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=False)