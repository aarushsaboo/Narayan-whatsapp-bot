import asyncpg
from env import NEON_DB_USER, NEON_DB_PASSWORD, NEON_DB_HOST, NEON_DB_PORT, NEON_DB_NAME

async def insert_in_db(name, phone_number, amount):
    try:
        dsn = f"postgresql://{NEON_DB_USER}:{NEON_DB_PASSWORD}@{NEON_DB_HOST}:{NEON_DB_PORT}/{NEON_DB_NAME}"
        conn = await asyncpg.connect(dsn)

        try:
            # Ensure phone number has +91 prefix
            formatted_phone = phone_number
            if not phone_number.startswith("+91"):
                formatted_phone = "+91" + phone_number

            query = """
                INSERT INTO transactions (name, phone_number, amount, transaction_date, payment_method, status)
                VALUES ($1, $2, $3, NOW(), 'UPI', 'SUCCESS')
            """
            await conn.execute(query, name, formatted_phone, amount)
            print("✅ Data inserted successfully!")
            return "Transaction saved."

        finally:
            await conn.close()

    except Exception as e:
        print(f"❌ Error inserting transaction: {e}")
        return "Error saving transaction."
