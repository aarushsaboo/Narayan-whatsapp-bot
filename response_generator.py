# response_generator.py
import asyncio
from datetime import datetime, timedelta
from google.genai import types
from env import DUMMY_DONATIONS, DONOR_EMAILS, LONG_CONTEXT, OFFICE_HOURS, CURRENT_CAMPAIGNS, GREETINGS
from message_analysis import detect_language, extract_info_from_query, identify_intent, get_user_id_from_info
from database import get_user_data, update_user_data
from utils.email_utils import handle_email_receipt_request
from utils.transaction_utils import get_latest_transaction

async def generate_response_async(query, sender_phone, client):
    model = "gemini-2.0-flash"

    lang_code, language_name = detect_language(query)
    
    extracted_info = extract_info_from_query(query)
    intent = identify_intent(query)

    if intent == "receipt_issue":
        return await handle_email_receipt_request(query, sender_phone, client)

    # Handle transaction verification
    if intent == "utr_verification":
        latest_transaction = await get_latest_transaction(sender_phone)
        if latest_transaction:
            return f"Yes, I can confirm your latest transaction of ₹{latest_transaction['amount']} on {latest_transaction['transaction_date'].strftime('%Y-%m-%d')} with transaction ID {latest_transaction['transaction_id']} has been received. Thank you for your support!"
        else:
            return "I couldn't find any recent transactions associated with your number. If you've made a donation recently, it may take some time to reflect in our system."

    user_phone = get_user_id_from_info(extracted_info, sender_phone)

    # Get conversation summary and preferred language from Neon DB
    conversation_summary, stored_language = await get_user_data(user_phone)
    
    # Use the stored language if available, otherwise use the detected language
    # This ensures we maintain the language across the conversation unless user switches
    preferred_language = stored_language if stored_language else language_name
    
    # If user is now using a different language than what's stored, update to the new language
    if stored_language and stored_language != language_name:
        preferred_language = language_name  # Update to the new language the user is using
    
    # Build user context with detailed information
    user_context = ""
    if user_phone and user_phone in DUMMY_DONATIONS and DUMMY_DONATIONS[user_phone]:
        user_context = f"\nDonor Information:\nName: {DUMMY_DONATIONS[user_phone][0].get('donor_name')}\nPhone: {user_phone}\nEmail: {DONOR_EMAILS.get(user_phone)}\n\nDonation History:\n"
        for d in DUMMY_DONATIONS[user_phone]:
            receipt_status = "Sent on " + (datetime.strptime(d.get('date'), "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d") if d.get("receipt_sent") else "Pending - Will be sent within 24 hours"
            user_context += f"- ₹{d.get('amount')} on {d.get('date')} for {d.get('campaign')}, via {d.get('payment_method')}, UTR: {d.get('utr')}, Receipt Status: {receipt_status}\n"
    else:
        user_context = "\nThis appears to be a new donor with no previous donation history in our system.\n"

    conversation_context = ""
    if conversation_summary:
        conversation_context = f"\nConversation Summary:\n{conversation_summary}\n"

    current_datetime = datetime.now().strftime("%Y-%m-%d, %A, %H:%M")
    time_context = f"\nCurrent Date and Time: {current_datetime}\nOffice Hours: {OFFICE_HOURS}\nActive Campaigns: {', '.join(CURRENT_CAMPAIGNS)}\n"

    greeting_templates = GREETINGS.get(preferred_language, GREETINGS["English"])
    greeting_context = f"\nGreeting templates for {preferred_language}:\n"
    greeting_context += "\n".join([f"- {key}: {value}" for key, value in greeting_templates.items()])

    system_instruction = f"""You are Ananya, a friendly and helpful receptionist at Narayan Shiva Sansthan, a charitable organization.
Your role is to assist donors, potential donors, and anyone with inquiries about the foundation via WhatsApp.
Always be warm, personable, and speak as if you're responding from our charity office.

IMPORTANT: The user is communicating in {preferred_language}. YOU MUST RESPOND IN {preferred_language} USING THE APPROPRIATE SCRIPT.
If the user message is in English, ALWAYS respond in English.
If the user is communicating in Hindi, respond in Hindi using Devanagari script (देवनागरी).
If the user is communicating in any other Indian language, respond in that language using its native script.

Use Indian expressions and references where appropriate. Address people respectfully, using "ji" occasionally.

Current information:
{time_context}

Donor information:
{user_context}

Previous conversation context:
{conversation_context}

Available greetings:
{greeting_context}

Foundation information:
{LONG_CONTEXT}

When starting a conversation:
- ONLY use greetings like "{greeting_templates.get('hello', 'Namaste!')}" or "{greeting_templates.get('intro', "I'm Ananya from Narayan Shiva Sansthan.")}" if the user's message is a short greeting like "hi", "hello", or "namaste".
- For all other messages, respond directly to the query without any introductory greeting.
- Thank donors for their support and generosity if they mention past donations.

IMPORTANT: Never include any "acting" or roleplay elements in your responses. Do not include phrases like "(slight pause)" or descriptions of your actions. Simply respond as if you're having a natural conversation. Keep your responses concise for WhatsApp.

Guidelines based on inquiry type:
1. For donation intents - Express gratitude, provide donation options, and the donation link (https://donate.narayanss.org)
2. For receipt issues - Check the donation history, apologize for any delays, and offer to expedite. If a UTR is provided, try to locate the donation.
3. For UTR verifications - Confirm transactions from the donation history if available.
4. For volunteer inquiries - Share volunteer opportunities and ask for their areas of interest. Provide contact info if needed (volunteer@narayanss.org).
5. For tax benefit inquiries - Explain Section 80G benefits clearly and what documentation we provide.
6. For office inquiries - Share our address and invite them to visit during office hours.
7. For project inquiries - Describe our current initiatives with enthusiasm and share brief success stories.

Important notes:
- Be compassionate and patient, especially with donation-related concerns.
- If you don't have certain information, offer to connect them with the appropriate team member or provide a contact number (+91 88888-55555).
- Always express gratitude for their interest in our foundation.
- End conversations warmly and ask if there's anything else you can assist with.
- Your responses should be concise and professional for WhatsApp.

Remember, you're the friendly voice of Narayan Shiva Sansthan Foundation on WhatsApp!
"""

    generate_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.7,
        max_output_tokens=1000,
    )

    contents = [query]
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_config
    )

    response_text = response.text if response.text else "Sorry, I couldn't generate a response at the moment."
    
    await update_user_data(user_phone, query, response_text, preferred_language, client)
    
    return response_text

def generate_response(query, sender_phone, client):
    return asyncio.run(generate_response_async(query, sender_phone, client))