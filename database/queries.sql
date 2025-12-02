-- Queries for Analysis

-- 1. Average Sentiment Score per Bank
SELECT 
    b.bank_name, 
    AVG(r.sentiment_score) as avg_sentiment,
    COUNT(*) as review_count
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name;

-- 2. Rating Distribution per Bank
SELECT 
    b.bank_name, 
    r.rating, 
    COUNT(*) as count
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name, r.rating
ORDER BY b.bank_name, r.rating DESC;

-- 3. Negative Reviews for specific bank (e.g., CBE)
SELECT review_text, sentiment_score
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
WHERE b.bank_name = 'CBE' AND r.sentiment_label = 'Negative'
ORDER BY r.sentiment_score ASC
LIMIT 10;
