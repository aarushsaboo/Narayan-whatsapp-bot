# Expanded dummy donation data with more realistic information
DUMMY_DONATIONS = {
    1: [
        {"amount": 3000, "date": "2025-03-02", "utr": "UTR789456", "receipt_sent": False, "donor_name": "Rajesh Sharma", "payment_method": "UPI", "campaign": "Education Fund"},
        {"amount": 5000, "date": "2024-12-15", "utr": "UTR123789", "receipt_sent": True, "donor_name": "Rajesh Sharma", "payment_method": "Bank Transfer", "campaign": "Winter Relief"}
    ],
    2: [
        {"amount": 10000, "date": "2025-04-01", "utr": "UTR456123", "receipt_sent": True, "donor_name": "Priya Patel", "payment_method": "Credit Card", "campaign": "Healthcare Initiative"},
        {"amount": 2500, "date": "2025-01-10", "utr": "UTR987234", "receipt_sent": True, "donor_name": "Priya Patel", "payment_method": "UPI", "campaign": "Education Fund"}
    ],
    3: [
        {"amount": 50000, "date": "2025-03-15", "utr": "UTR567890", "receipt_sent": False, "donor_name": "Amit Verma", "payment_method": "Bank Transfer", "campaign": "Rural Development"},
        {"amount": 15000, "date": "2024-11-05", "utr": "UTR345678", "receipt_sent": True, "donor_name": "Amit Verma", "payment_method": "UPI", "campaign": "Clean Water Project"}
    ],
    4: [
        {"amount": 1000, "date": "2025-03-28", "utr": "UTR654321", "receipt_sent": True, "donor_name": "Sneha Gupta", "payment_method": "UPI", "campaign": "Education Fund"}
    ],
    5: [],  # New donor with no history
    6: [
        {"amount": 2000, "date": "2025-02-18", "utr": "UTR123456", "receipt_sent": True, "donor_name": "Arvin Kumar", "payment_method": "UPI", "campaign": "Education Fund"}
    ]
}

# Phone numbers for dummy data
DONOR_PHONE_NUMBERS = {
    1: "+91 98765 43210",
    2: "+91 87654 32109",
    3: "+91 76543 21098",
    4: "+91 65432 10987",
    5: "+91 54321 09876",
    6: "+91 97800 86800"
}

# Email addresses for dummy data
DONOR_EMAILS = {
    1: "rajesh.sharma@example.com",
    2: "priya.patel@example.com",
    3: "amit.verma@example.com",
    4: "sneha.gupta@example.com",
    5: "new.donor@example.com",
    6: "arvin.kumar@example.com"
}

# Enhanced context for the assistant
LONG_CONTEXT = """
Narayan Shiva Sansthan:

ABOUT US:
- Narayan Shiva Sansthan is a registered charitable organization (Reg. No. CHT/2008/45678)
- Founded in 2008 with a mission to create sustainable impact across underserved communities
- 95% of donations go directly to our programs and beneficiaries
- Transparent financial reporting available on our website quarterly

DONATION OPTIONS:
- UPI: donations@NarayanShivaSansthan
- Credit/Debit Cards: Processed securely through our payment gateway
- Bank Transfer: Account No: 12345678901, IFSC: HDHF0001234, Narayan Shiva Sansthan
- Cheque: Payable to "Narayan Shiva Sansthan" and mailed to our office
- Monthly recurring donations available with a minimum of ₹100/month

TAX BENEFITS:
- All donations are eligible for tax benefits under Section 80G
- Tax receipts are automatically generated for donations above ₹500
- For donations above ₹50,000, additional KYC documentation is required (PAN card copy)
- Foreign donations are processed under FCRA regulations

PROJECTS AND CAMPAIGNS:
1. Education Fund: Supports scholarships and school infrastructure in rural areas
2. Healthcare Initiative: Mobile medical camps and primary healthcare centers
3. Rural Development: Skill training, microfinance, and sustainable farming practices
4. Clean Water Project: Installing water purification systems in villages
5. Winter Relief: Blankets and warm clothing distribution in northern regions
6. Disaster Response: Emergency relief during natural calamities

DONOR SERVICES:
- Receipts are typically sent within 24-48 hours of donation confirmation
- Donors can track their donations using UTR numbers through our online portal
- Regular impact reports are sent to all donors quarterly
- Donor helpdesk available Monday-Saturday (10am-6pm) at +91 88888-55555
- For urgent receipt issues, contact receipts@narayanss.org

VOLUNTEERING:
- Volunteer opportunities available across all our projects
- Corporate volunteering programs for team-building activities
- Weekend volunteering drives in local communities
- Register as a volunteer at volunteer@narayanss.org

OFFICE ADDRESS:
Narayan Shiva Sansthan
123 Charity Lane, Saket
New Delhi - 110017
"""

OFFICE_HOURS = "Monday to Saturday, 10:00 AM to 6:00 PM"
CURRENT_CAMPAIGNS = ["Education Fund", "Healthcare Initiative", "Clean Water Project", "Summer Relief 2025"]

# Multi-language greeting templates
GREETINGS = {
    "Hindi": {
        "hello": "नमस्ते!",
        "intro": "मैं नारायण शिव संस्थान से अनन्या हूँ।",
        "welcome": "नारायण शिव संस्थान में आपका स्वागत है!",
        "thank_you": "आपके समर्थन के लिए धन्यवाद।"
    },
    "English": {
        "hello": "Hello!",
        "intro": "I'm Ananya from Narayan Shiva Sansthan.",
        "welcome": "Welcome to Narayan Shiva Sansthan!",
        "thank_you": "Thank you for your support."
    },
    "Marathi": {
        "hello": "नमस्कार!",
        "intro": "मी नारायण शिव संस्थानची अनन्या आहे.",
        "welcome": "नारायण शिव संस्थानमध्ये आपले स्वागत आहे!",
        "thank_you": "आपल्या समर्थनासाठी धन्यवाद."
    },
    "Gujarati": {
        "hello": "નમસ્તે!",
        "intro": "હું નારાયણ શિવ સંસ્થાનથી અનન્યા છું.",
        "welcome": "નારાયણ શિવ સંસ્થાનમાં આપનું સ્વાગત છે!",
        "thank_you": "આપના સમર્થન બદલ આભાર."
    },
    "Tamil": {
        "hello": "வணக்கம்!",
        "intro": "நான் நாராயண சிவ சன்ஸ்தானில் இருந்து அனன்யா.",
        "welcome": "நாராயண சிவ சன்ஸ்தானுக்கு வரவேற்கிறோம்!",
        "thank_you": "உங்கள் ஆதரவுக்கு நன்றி."
    },
    "Telugu": {
        "hello": "నమస్కారం!",
        "intro": "నేను నారాయణ శివ సంస్థాన్ నుండి అనన్య.",
        "welcome": "నారాయణ శివ సంస్థాన్‌కి స్వాగతం!",
        "thank_you": "మీ మద్దతుకు ధన్యవాదాలు."
    },
    "Bengali": {
        "hello": "নমস্কার!",
        "intro": "আমি নারায়ণ শিব সংস্থান থেকে অনন্যা।",
        "welcome": "নারায়ণ শিব সংস্থানে আপনাকে স্বাগতম!",
        "thank_you": "আপনার সমর্থনের জন্য ধন্যবাদ।"
    },
    "Punjabi": {
        "hello": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ!",
        "intro": "ਮੈਂ ਨਾਰਾਇਣ ਸ਼ਿਵ ਸੰਸਥਾਨ ਤੋਂ ਅਨੰਨਿਆ ਹਾਂ।",
        "welcome": "ਨਾਰਾਇਣ ਸ਼ਿਵ ਸੰਸਥਾਨ ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ!",
        "thank_you": "ਤੁਹਾਡੇ ਸਮਰਥਨ ਲਈ ਧੰਨਵਾਦ।"
    }
}