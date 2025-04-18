import uuid, asyncpg
from env import NEON_DB_USER, NEON_DB_PASSWORD, NEON_DB_HOST, NEON_DB_PORT, NEON_DB_NAME

async def insert_in_db(name, phone_number, amount):
    # 1️⃣ Build your DSN & connect
    dsn = f"postgresql://{NEON_DB_USER}:{NEON_DB_PASSWORD}@{NEON_DB_HOST}:{NEON_DB_PORT}/{NEON_DB_NAME}"
    conn = await asyncpg.connect(dsn)

    try:
        # 3️⃣ Generate a VARCHAR(20) transaction_id
        txn_id = uuid.uuid4().hex[:20]  # e.g. '9f8c7b6a5d4e3f2a1b0c'

        # 4️⃣ Your corrected query (note user_name instead of name)
        query = """
            INSERT INTO transactions (
                transaction_id,
                user_name,
                phone_number,
                amount,
                transaction_date,
                payment_method,
                status
            )
            VALUES ($1, $2, $3, $4, NOW(), 'UPI', 'SUCCESS')
        """

        # 5️⃣ Pass exactly 4 params → $1=txn_id, $2=name, $3=phone, $4=amount
        await conn.execute(query, txn_id, name, phone_number, amount)

        print("✅ Data inserted successfully!")
        return "Transaction saved."
    finally:
        await conn.close()
