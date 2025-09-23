-- Watermark control table
CREATE OR REPLACE TABLE load_process_watermark (
    source_table STRING,
    last_successful_watermark TIMESTAMP
);

-- Target integration table
CREATE OR REPLACE TABLE sales_integration (
    id INT,
    customer_id INT,
    amount DECIMAL(10,2),
    sale_date TIMESTAMP
);

-- Load new rows only
INSERT INTO sales_integration
SELECT *
FROM sales_raw
WHERE sale_date > (
    SELECT COALESCE(MAX(last_successful_watermark), '1900-01-01')
    FROM load_process_watermark
    WHERE source_table = 'SALES_RAW'
);

-- Update watermark
MERGE INTO load_process_watermark t
USING (SELECT 'SALES_RAW' AS source_table, MAX(sale_date) AS new_wm FROM sales_raw) s
ON t.source_table = s.source_table
WHEN MATCHED THEN UPDATE SET t.last_successful_watermark = s.new_wm
WHEN NOT MATCHED THEN INSERT (source_table, last_successful_watermark) VALUES (s.source_table, s.new_wm);
