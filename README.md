CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(20) NOT NULL UNIQUE,
    user_id INTEGER,
    user_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    payment_method VARCHAR(30),
    status VARCHAR(20) DEFAULT 'Completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on phone_number for faster lookups
CREATE INDEX IF NOT EXISTS idx_transactions_phone ON transactions(phone_number);
-- Create an index on transaction_date for sorting
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);