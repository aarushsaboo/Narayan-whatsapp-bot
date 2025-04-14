# check_neondb.py
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database connection parameters
NEON_DB_USER = os.getenv("NEON_DB_USER")
NEON_DB_PASSWORD = os.getenv("NEON_DB_PASSWORD")
NEON_DB_HOST = os.getenv("NEON_DB_HOST")
NEON_DB_PORT = os.getenv("NEON_DB_PORT")
NEON_DB_NAME = os.getenv("NEON_DB_NAME")

async def check_connection():
    print("Attempting to connect to Neon database...")
    print(f"Host: {NEON_DB_HOST}")
    print(f"Database: {NEON_DB_NAME}")
    print(f"User: {NEON_DB_USER}")
    
    try:
        # Connect to database
        conn = await asyncpg.connect(
            user=NEON_DB_USER,
            password=NEON_DB_PASSWORD,
            database=NEON_DB_NAME,
            host=NEON_DB_HOST,
            port=NEON_DB_PORT
        )
        
        print("Connection successful! ✅")
        
        # Check for existing tables
        tables = await conn.fetch(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )
        
        if tables:
            print("\nExisting tables:")
            for table in tables:
                print(f"- {table['table_name']}")
                
                # Get column info for each table
                columns = await conn.fetch(
                    "SELECT column_name, data_type FROM information_schema.columns "
                    f"WHERE table_name = '{table['table_name']}'"
                )
                for col in columns:
                    print(f"  • {col['column_name']} ({col['data_type']})")
        else:
            print("\nNo tables found in database.")
        
        await conn.close()
        
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

async def create_tables():
    print("\nCreating necessary tables...")
    try:
        conn = await asyncpg.connect(
            user=NEON_DB_USER,
            password=NEON_DB_PASSWORD,
            database=NEON_DB_NAME,
            host=NEON_DB_HOST,
            port=NEON_DB_PORT
        )
        
        # Create logs table for conversation summaries
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            phone VARCHAR(20) UNIQUE NOT NULL,
            summary TEXT,
            preferred_language VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        print("Tables created successfully! ✅")
        await conn.close()
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

async def main():
    connection_successful = await check_connection()
    
    if connection_successful:
        await create_tables()
    else:
        print("Please check your database credentials and try again.")

if __name__ == "__main__":
    asyncio.run(main())