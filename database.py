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

async def get_conversation_summary(phone_number):
    conn = None
    try:
        conn = await connect_to_neon()
        if not conn:
            print("Failed to connect to database")
            return None
        
        row = await conn.fetchrow("SELECT summary FROM logs WHERE phone = $1", phone_number)
        
        if row:
            return row['summary']
        return None
    except Exception as e:
        print(f"Error fetching conversation summary: {e}")
        return None
    finally:
        if conn:
            await conn.close()

async def update_conversation_summary(phone_number, user_message, ai_response, client):
    conn = None
    try:
        conn = await connect_to_neon()
        if not conn:
            print("Failed to connect to database")
            return False
        
        row = await conn.fetchrow("SELECT summary FROM logs WHERE phone = $1", phone_number)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                "UPDATE logs SET summary = $1 WHERE phone = $2",
                summary_response, phone_number
            )
        else:
            summary = f"Summary of conversation so far: Initial contact from user. Last message from user: {user_message}"
            
            await conn.execute(
                "INSERT INTO logs (phone, summary) VALUES ($1, $2)",
                phone_number, summary
            )
            
            summary_response = summary
        
        return summary_response
    except Exception as e:
        print(f"Error updating conversation summary: {e}")
        return None
    finally:
        if conn:
            await conn.close()