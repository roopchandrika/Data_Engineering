-- Create table
CREATE OR REPLACE TABLE sales_raw (
    id INT,
    customer_id INT,
    amount DECIMAL(10,2),
    sale_date TIMESTAMP
);

-- Generate 1M rows (using Snowflake's generator)
INSERT INTO sales_raw
SELECT SEQ4(), UNIFORM(1,10000,RANDOM()), UNIFORM(10,500,RANDOM()), CURRENT_TIMESTAMP()
FROM TABLE(GENERATOR(ROWCOUNT => 1000000));


-- Test Clustering
ALTER TABLE sales_raw CLUSTER BY (customer_id);

-- Check Performance

SELECT customer_id, SUM(amount)
FROM sales_raw
WHERE customer_id = 1234
GROUP BY customer_id;
