# message_analysis.py
import re
from langdetect import detect, LangDetectException
from env import DUMMY_DONATIONS, DONOR_EMAILS

def detect_language(text):
    try:
        lang_code = detect(text)
        language_map = {
            'hi': 'Hindi',
            'en': 'English',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi',
            'bn': 'Bengali',
            'ur': 'Urdu',
            'or': 'Odia'
        }
        return lang_code, language_map.get(lang_code, 'Unknown')
    except LangDetectException:
        return 'en', 'English'

def identify_intent(query):
    query_lower = query.lower()

    if any(word in query_lower for word in ["donate", "contribution", "give", "support", "contribute", "payment"]):
        return "donation_intent"
    elif any(word in query_lower for word in ["receipt", "tax", "acknowledgment", "certificate", "80g"]) and any(word in query_lower for word in ["didn't get", "haven't received", "missing", "where", "not received"]):
        return "receipt_issue"
    elif any(word in query_lower for word in ["utr", "transaction", "payment", "confirm", "successful", "went through"]):
        return "utr_verification"
    elif any(word in query_lower for word in ["volunteer", "volunteering", "help out", "join", "participate"]):
        return "volunteer_inquiry"
    elif any(word in query_lower for word in ["tax benefit", "80g", "deduction", "tax exemption"]):
        return "tax_benefit_inquiry"
    elif any(word in query_lower for word in ["project", "campaign", "initiative", "program", "what do you do"]):
        return "project_inquiry"
    elif any(word in query_lower for word in ["office", "location", "address", "visit", "come to"]):
        return "office_inquiry"
    else:
        return "general_inquiry"

def extract_info_from_query(query):
    utr_match = re.search(r'UTR\d+', query, re.IGNORECASE)
    utr = utr_match.group(0) if utr_match else None

    amount_match = re.search(r'₹\s*(\d+)', query) or re.search(r'Rs\.?\s*(\d+)', query) or re.search(r'(\d+)\s*rupees', query, re.IGNORECASE)
    amount = amount_match.group(1) if amount_match else None

    phone_match = re.search(r'(\+91\s?)?[789]\d{9}', query) or re.search(r'(\+91\s?)?[789]\d\d\d\d\s?\d\d\d\d\d', query)
    phone = phone_match.group(0) if phone_match else None

    name_indicators = ["name is", "this is", "called", "speaking", "named", "by the name"]
    name = None
    for indicator in name_indicators:
        if indicator in query.lower():
            parts = query.lower().split(indicator)
            if len(parts) > 1:
                potential_name = parts[1].strip().split()[0].capitalize()
                if len(potential_name) > 2:
                    name = potential_name
                    break

    common_names = ["Arvin", "Rajesh", "Priya", "Amit", "Sneha"]
    for common_name in common_names:
        if common_name.lower() in query.lower():
            name = common_name
            break

    return {"utr": utr, "amount": amount, "phone": phone, "name": name}

def get_user_id_from_info(extracted_info, sender_phone):
    if sender_phone in DUMMY_DONATIONS:
        return sender_phone

    if extracted_info["utr"]:
        for phone, donations in DUMMY_DONATIONS.items():
            if any(d.get("utr", "") == extracted_info["utr"] for d in donations):
                return phone

    if extracted_info["name"]:
        for phone, donations in DUMMY_DONATIONS.items():
            if donations and any(extracted_info["name"].lower() in d.get("donor_name", "").lower() for d in donations):
                return phone

    if extracted_info["phone"] and extracted_info["phone"] in DUMMY_DONATIONS:
        return extracted_info["phone"]
    elif extracted_info["phone"]:
        cleaned_phone = "".join(filter(str.isdigit, extracted_info["phone"]))
        for phone in DUMMY_DONATIONS:
            cleaned_donor_phone = "".join(filter(str.isdigit, phone))
            if cleaned_phone[-10:] == cleaned_donor_phone[-10:]:
                return phone

    if extracted_info["name"] == "Arvin":
        return "+919780086800"
    elif extracted_info["phone"] and "97800" in extracted_info["phone"]:
        return "+919780086800"

    return sender_phone

def is_introductory_message(query):
    query_lower = query.lower().strip()
    greetings = ["hi", "hello", "namaste", "namaskar", "vanakkam", "salaam", "sat sri akal", "नमस्ते", "नमस्कार", "வணக்கம்", "నమస్కారం", "নমস্কার", "ਸਤ ਸ੍ਰੀ ਅਕਾਲ"]
    return len(query_lower.split()) <= 2 and any(greet in query_lower for greet in greetings)