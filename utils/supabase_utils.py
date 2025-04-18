# utils/supabase_utils.py
from supabase import create_client, Client
from datetime import datetime
import os

# Supabase Client Setup
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://cmdnmsafreigvaatmkub.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNtZG5tc2FmcmVpZ3ZhYXRta3ViIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NDk4MzgxNCwiZXhwIjoyMDYwNTU5ODE0fQ.r4w6mZyu03aD7YFtQQ9Pd6pBY2D2XHP0ChVEgIRcZvk")

def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_pdf_to_supabase(pdf_bytes, phone_number=None):
    """Upload PDF bytes to Supabase storage and return a signed URL"""
    try:
        # Create unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        identifier = phone_number[-4:] if phone_number else "unknown"
        filename = f"receipt_{identifier}_{timestamp}.pdf"
        
        # Get Supabase client
        supabase = get_supabase_client()
        
        # Upload file
        upload_response = supabase.storage.from_("pdfs").upload(
            path=f"files/{filename}",
            file=pdf_bytes,
            file_options={"content-type": "application/pdf"}
        )
        
        # Generate signed URL
        signed_url_response = supabase.storage.from_("pdfs").create_signed_url(
            path=f"files/{filename}",
            expires_in=86400  # 24 hours expiry
        )
        
        return signed_url_response["signedURL"]
    except Exception as e:
        print(f"Supabase upload error: {str(e)}")
        # Return fallback URL in case of error
        return "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"