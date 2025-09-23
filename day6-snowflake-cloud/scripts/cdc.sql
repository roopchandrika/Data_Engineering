-- Base table
CREATE OR REPLACE TABLE customers (
    id INT,
    name STRING,
    updated_at TIMESTAMP
);

-- Stream to capture CDC
CREATE OR REPLACE STREAM customers_stream ON TABLE customers;

-- Target table
CREATE OR REPLACE TABLE customers_cdc (
    id INT,
    name STRING,
    updated_at TIMESTAMP,
    change_type STRING
);

-- Task to apply changes every 5 minutes
CREATE OR REPLACE TASK customers_cdc_task
WAREHOUSE = COMPUTE_WH
SCHEDULE = '5 MINUTE'
AS
INSERT INTO customers_cdc
SELECT id, name, updated_at, metadata$action
FROM customers_stream;
