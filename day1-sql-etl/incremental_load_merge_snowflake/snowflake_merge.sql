-- =========================================================
-- Snowflake Incremental Load Demo (Staging + MERGE Pattern)
-- =========================================================

-- 1. Create database and schemas
CREATE DATABASE IF NOT EXISTS etl_demo;
USE DATABASE etl_demo;

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS integration;

-- 2. Create staging and final tables
CREATE OR REPLACE TABLE raw.users_stage (
    id INT,
    name STRING,
    email STRING,
    updated_at TIMESTAMP
);

CREATE OR REPLACE TABLE integration.users_final LIKE raw.users_stage;

-- 3. Insert first batch into staging
INSERT INTO raw.users_stage VALUES
  (1, 'Alice', 'alice@test.com', '2025-09-15 10:00'),
  (2, 'Bob', 'bob@test.com', '2025-09-15 10:00');

-- 4. Run initial MERGE (all rows inserted into final)
MERGE INTO integration.users_final tgt
USING raw.users_stage src
ON tgt.id = src.id
WHEN MATCHED AND src.updated_at > tgt.updated_at THEN
    UPDATE SET
        name = src.name,
        email = src.email,
        updated_at = src.updated_at
WHEN NOT MATCHED THEN
    INSERT (id, name, email, updated_at)
    VALUES (src.id, src.name, src.email, src.updated_at);

-- Check results
SELECT * FROM integration.users_final;

-- 5. Insert second batch (Bob updated, Charlie new)
INSERT INTO raw.users_stage VALUES
  (2, 'Bob Updated', 'bob@test.com', '2025-09-15 12:00'),
  (3, 'Charlie', 'charlie@test.com', '2025-09-15 12:00');

-- 6. Run MERGE again (Bob updated, Charlie inserted)
MERGE INTO integration.users_final tgt
USING raw.users_stage src
ON tgt.id = src.id
WHEN MATCHED AND src.updated_at > tgt.updated_at THEN
    UPDATE SET
        name = src.name,
        email = src.email,
        updated_at = src.updated_at
WHEN NOT MATCHED THEN
    INSERT (id, name, email, updated_at)
    VALUES (src.id, src.name, src.email, src.updated_at);

-- 7. Validation queries
-- Total rows
SELECT COUNT(*) AS total_rows FROM integration.users_final;

-- Bob should show updated version
SELECT * FROM integration.users_final WHERE id = 2;

-- Latest updated_at per user
SELECT id, MAX(updated_at) AS latest_update
FROM integration.users_final
GROUP BY id;
