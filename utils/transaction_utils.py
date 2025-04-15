import asyncio
import asyncpg 
from env import NEON_DB_USER, NEON_DB_PASSWORD, NEON_DB_HOST, NEON_DB_PORT, NEON_DB_NAME

async def get_latest_transaction_async(user_phone):
    try:
        dsn = f"postgresql://{NEON_DB_USER}:{NEON_DB_PASSWORD}@{NEON_DB_HOST}:{NEON_DB_PORT}/{NEON_DB_NAME}"
        
        # Connect to the database
        conn = await asyncpg.connect(dsn)
        
        try:
            # Query to get the latest transaction for this phone number
            query = """
                SELECT 
                    id, 
                    transaction_id, 
                    user_id,
                    user_name,
                    phone_number,
                    email,
                    amount::text, 
                    transaction_date, 
                    payment_method,
                    status
                FROM transactions 
                WHERE phone_number = $1 
                ORDER BY transaction_date DESC 
                LIMIT 1
            """
            
            # Execute the query
            row = await conn.fetchrow(query, user_phone)
            
            # If no transaction found
            if not row:
                return None
                
            # Convert row to dictionary
            transaction = dict(row)
            
            # Convert amount to float
            transaction['amount'] = float(transaction['amount'])
            
            return transaction
            
        finally:
            await conn.close()
            
    except Exception as e:
        print(f"Error retrieving transaction: {e}")
        return None

def get_latest_transaction(user_phone):
    return get_latest_transaction_async(user_phone)