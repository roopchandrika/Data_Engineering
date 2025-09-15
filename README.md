# 📘 Day 1 – SQL Mastery & Incremental Load

## 🎯 Objectives

* Strengthen SQL fundamentals (joins, window functions, aggregations, CTEs).
* Solve 10 SQL problems (LeetCode).
* Build 2 ETL pipelines:

  1. API → CSV → Postgres
  2. Incremental load with MERGE in Snowflake

---

## 🛠️ Skills Covered

* **SQL**: Joins, Window Functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`), Aggregations, CTEs
* **ETL Development**: API extraction, CSV staging, Postgres load
* **Data Warehousing**: Incremental load and CDC with Snowflake MERGE
* **Tools**: Python, Pandas, SQLAlchemy, Docker (Postgres), Snowflake

---

## 📚 Step 1 – SQL Fundamentals & Practice

* Reviewed key SQL concepts: Joins, Window Functions, CTEs, Aggregations.
* Solved **10 curated LeetCode SQL problems** (joins, window functions, subqueries, aggregations).
* These covered real-world interview patterns like *Nth Highest Salary*, *Department Highest Salary*, and *Delete Duplicate Emails*.

📌 Note: Solutions are practiced locally but not included in this repo.

---

## 🔄 Step 2 – Pipeline #1 (API → CSV → Postgres)

### Extract (API → CSV)

**File:** `pipelines/api_extract.py`

* Fetches 50 random users from Random User API
* Flattens JSON using Pandas
* Saves data into `data/users.csv`

### Load (CSV → Postgres)

**File:** `pipelines/load_postgres.py`

* Reads `users.csv` → Pandas DataFrame
* Connects to Postgres via SQLAlchemy
* Loads into table `users`

### Run Postgres (Docker)

```bash
docker run --name pg-sql-day1 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=etl_demo \
  -p 5433:5432 -d postgres
```

### Verify in Postgres

```sql
\dt
SELECT COUNT(*) FROM users;
SELECT * FROM users LIMIT 5;
```

---

## 🔄 Step 3 – Pipeline #2 (Incremental Load with Snowflake MERGE)

### Setup

```sql
CREATE DATABASE IF NOT EXISTS etl_demo;
USE DATABASE etl_demo;

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS integration;
```

### Tables

```sql
CREATE OR REPLACE TABLE raw.users_stage (
    id INT,
    name STRING,
    email STRING,
    updated_at TIMESTAMP
);

CREATE OR REPLACE TABLE integration.users_final LIKE raw.users_stage;
```

### First Batch

```sql
INSERT INTO raw.users_stage VALUES
  (1, 'Alice', 'alice@test.com', '2025-09-15 10:00'),
  (2, 'Bob', 'bob@test.com', '2025-09-15 10:00');
```

### MERGE Logic

```sql
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
```

### Incremental Batch

```sql
INSERT INTO raw.users_stage VALUES
  (2, 'Bob Updated', 'bob@test.com', '2025-09-15 12:00'),
  (3, 'Charlie', 'charlie@test.com', '2025-09-15 12:00');
```

Re-run MERGE →

* Alice (unchanged)
* Bob (updated)
* Charlie (new row)

### Validation Queries

```sql
SELECT COUNT(*) FROM integration.users_final;
SELECT * FROM integration.users_final WHERE id = 2;
SELECT id, MAX(updated_at) FROM integration.users_final GROUP BY id;
```

📂 Script: [`sql_problems/snowflake_merge.sql`](./sql_problems/snowflake_merge.sql)

---

## 🚀 Deliverables

* Practiced 10 SQL problems (not shared in repo, but documented).
* Built **API → CSV → Postgres pipeline**.
* Built **Incremental load with MERGE in Snowflake**.
* Scripts in `pipelines/` and `sql_problems/`.
* Dockerized Postgres setup instructions.

---

## ✅ End of Day 1

* Practiced SQL deeply
* Built 2 ETL pipelines
* Documented **incremental load with MERGE** (common interview scenario)

---
