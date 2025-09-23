# Day 6 – Cloud Hands-On (Snowflake + ADF)

This folder documents the work for **Day 6**: building a cloud pipeline using **Azure Data Factory (ADF)** and **Snowflake**, including **incremental load** and **CDC with Streams & Tasks**.

---

## 🚀 Setup & Versions
- **Snowflake Edition**: Free Trial
- **Azure Data Factory**: Free Trial workspace
- **Authentication**: SAS Token for Blob, Username/Password for Snowflake
- **Warehouse**: COMPUTE_WH
- **Database**: ADF_DB
- **Schema**: PUBLIC

---

## 🔹 Step 1 – Snowflake Setup

```sql
CREATE OR REPLACE DATABASE ADF_DB;
CREATE OR REPLACE SCHEMA PUBLIC;

CREATE OR REPLACE TABLE SALES_RAW (
    USER_ID INT,
    TRANSACTION_TYPE STRING,
    AMOUNT DOUBLE
);

CREATE OR REPLACE TABLE SALES_INTEGRATION (
    USER_ID INT,
    TRANSACTION_TYPE STRING,
    AMOUNT DOUBLE,
    LOAD_TS TIMESTAMP
);

CREATE OR REPLACE TABLE LOAD_PROCESS_WATERMARK (
    SOURCE_SYSTEM STRING,
    INTEGRATION_TABLE_NAME STRING,
    LAST_SUCCESSFUL_WATERMARK TIMESTAMP
);

INSERT INTO LOAD_PROCESS_WATERMARK
VALUES ('ADF_PIPELINE', 'SALES_INTEGRATION', '1970-01-01 00:00:00');

🔹 Step 2 – ADF Pipeline

Create Linked Services:

Blob Storage (SAS Authentication)

Snowflake

Create Datasets:

Blob_Transactions → source CSV

Snowflake_Sales_Raw → table SALES_RAW

Pipeline:

Copy Data Activity → Blob → Snowflake

Script Activity → run stored procedure

Debug + Publish + Schedule Trigger

🔹 Step 3 – Incremental Load

Stored procedure INCREMENTAL_LOAD_SALES:

Reads watermark from LOAD_PROCESS_WATERMARK

Inserts only new rows into SALES_INTEGRATION

Updates watermark

Returns status

🔹 Step 4 – CDC with Streams & Tasks
CREATE OR REPLACE STREAM SALES_RAW_STREAM ON TABLE SALES_RAW;

CREATE OR REPLACE TASK TASK_LOAD_SALES
WAREHOUSE = COMPUTE_WH
SCHEDULE = 'USING CRON 0 * * * * UTC'
AS
INSERT INTO SALES_INTEGRATION (USER_ID, TRANSACTION_TYPE, AMOUNT, LOAD_TS)
SELECT USER_ID, TRANSACTION_TYPE, AMOUNT, CURRENT_TIMESTAMP
FROM SALES_RAW_STREAM;

ALTER TASK TASK_LOAD_SALES RESUME;

✅ Achievements

Connected ADF → Snowflake

Loaded data from Blob CSV → SALES_RAW

Built Incremental Load using watermark

Implemented CDC with Streams + Tasks

Automated load pipeline with triggers

📌 Next Steps

Test performance with 1M+ rows

Explore Clustering & Query Tuning in Snowflake

Add Monitoring & Alerts in ADF

Extend to AWS Glue as alternative