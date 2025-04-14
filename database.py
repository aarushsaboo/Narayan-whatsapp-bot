# database.py
import asyncpg
from datetime import datetime
from env import NEON_DB_USER, NEON_DB_PASSWORD, NEON_DB_NAME, NEON_DB_HOST, NEON_DB_PORT

async def connect_to_neon():
    try:
        return await asyncpg.connect(
            user=NEON_DB_USER,
            password=NEON_DB_PASSWORD,
            database=NEON_DB_NAME,
            host=NEON_DB_HOST,
            port=NEON_DB_PORT
        )
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

async def get_user_data(phone_number):
    conn = None
    try:
        conn = await connect_to_neon()
        if not conn:
            print("Failed to connect to database")
            return None, None
        
        row = await conn.fetchrow("SELECT summary, preferred_language FROM logs WHERE phone = $1", phone_number)
        
        if row:
            return row['summary'], row['preferred_language']
        return None, None
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None, None
    finally:
        if conn:
            await conn.close()

async def update_user_data(phone_number, user_message, ai_response, detected_language, client):
    conn = None
    try:
        conn = await connect_to_neon()
        if not conn:
            print("Failed to connect to database")
            return False
        
        # Get current timestamp
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if we have a record for this phone number
        row = await conn.fetchrow("SELECT summary, preferred_language FROM logs WHERE phone = $1", phone_number)
        
        new_log_entry = f"[{timestamp}] User: {user_message} | Assistant: {ai_response}"
        
        if row:
            existing_summary = row['summary']
            
            prompt = (
                f"Based on this previous conversation summary: '{existing_summary}' "
                f"and this new exchange - User: '{user_message}' and Assistant: '{ai_response}', "
                f"provide a concise updated summary of the conversation so far. "
                f"Keep important details about the user's needs and context. "
                f"Format as 'Summary of conversation so far: [your summary]. Last message from user: {user_message}'"
            )
            
            summary_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt]
            ).text.strip()
            
            await conn.execute(
                "UPDATE logs SET summary = $1, preferred_language = $2, updated_at = $3 WHERE phone = $4",
                summary_response, detected_language, current_time, phone_number
            )
        else:
            summary = f"Summary of conversation so far: Initial contact from user. Last message from user: {user_message}"
            
            await conn.execute(
                "INSERT INTO logs (phone, summary, preferred_language, created_at, updated_at) VALUES ($1, $2, $3, $4, $5)",
                phone_number, summary, detected_language, current_time, current_time
            )
            
            summary_response = summary
        
        return summary_response
    except Exception as e:
        print(f"Error updating user data: {e}")
        return None
    finally:
        if conn:
            await conn.close()