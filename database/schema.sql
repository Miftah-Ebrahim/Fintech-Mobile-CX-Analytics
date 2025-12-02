-- Drop tables if they exist to ensure clean state
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS banks;

-- Create Banks Table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(50) UNIQUE NOT NULL,
    app_name VARCHAR(100)
);

-- Create Reviews Table
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT,
    rating INTEGER,
    review_date TIMESTAMP,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    source VARCHAR(50) DEFAULT 'Google Play'
);

-- Indexes for performance
CREATE INDEX idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX idx_reviews_date ON reviews(review_date);