# 🚀 7-Day Data Engineering Brush-Up Challenge

This repository documents my **7-day sprint to refresh core Data Engineering skills** — covering SQL, Python, PySpark, Airflow, Kafka, Snowflake, Data Modeling, and Data Quality/Governance.  

Each day’s work is tracked under a separate branch in GitHub for clarity:  
🔗 [Data_Engineering Repo](https://github.com/roopchandrika/Data_Engineering)

---

## 📌 Day-by-Day Progress

### **Day 1 – SQL Mastery**
- Reviewed joins, window functions, CTEs, and aggregations.
- Solved advanced SQL practice problems.
- **Pipelines Built:**
  - API → CSV → Postgres
  - Incremental MERGE load → Snowflake

---

### **Day 2 – Python + PySpark Basics**
- Focused on Python ETL patterns (logging, error handling).
- Practiced PySpark transformations (select, filter, groupBy).
- **Pipelines Built:**
  - CSV → Parquet
  - Parquet → Delta → Snowflake

---

### **Day 3 – Data Modeling + Warehousing**
- Studied Star Schema, Snowflake Schema, and Slowly Changing Dimensions (SCD).
- Designed schema for an e-commerce dataset (Orders, Customers, Products).
- **Pipelines Built:**
  - CSV → Snowflake staging
  - dbt models: bronze → silver → gold

---

### **Day 4 – Orchestration (Airflow)**
- Learned Airflow concepts: DAGs, Operators, retries, task dependencies, and Sensors.
- Deployed Airflow with Docker Compose.
- **Pipelines Built:**
  - CSV → Postgres
  - API → Postgres
  - Postgres → dbt transformations

---

### **Day 5 – Streaming (Kafka Basics)**
- Understood Kafka concepts: producers, consumers, partitions, offsets.
- Ran Kafka locally with Docker Compose.
- **Pipelines Built:**
  - Kafka producer (transactions)
  - Kafka consumer → Postgres
  - Kafka → Spark Structured Streaming → Delta

---

### **Day 6 – Cloud Hands-On (Snowflake + ADF/Glue)**
- Practiced Snowflake advanced features: streams, tasks, clustering, tuning.
- Loaded 1M+ rows into Snowflake and tested query performance.
- **Pipelines Built:**
  - Incremental load with watermark
  - CDC with Snowflake streams & tasks
  - ADF/Glue → Snowflake

---

### **Day 7 – Data Quality & Governance**
- Focused on ensuring **trust in data** using Great Expectations (GX).
- Built Airflow-integrated GX validation pipelines.
- Implemented RBAC roles + column masking in Snowflake.
- **Pipelines Built:**
  - Airflow DAG with GX checkpoints (null checks, duplicates, ranges)
  - Governance demo with Snowflake masking

---

## ✅ Key Outcomes
- **Pipelines built:** 18+ across SQL, Python, PySpark, Airflow, Kafka, Snowflake, and Great Expectations.  
- **Focus areas covered:** Data ingestion, transformation, orchestration, streaming, cloud, quality, and governance.  
- Practiced full **end-to-end Data Engineering lifecycle**: from raw ingestion → governed, trusted datasets.  

---

## 🔥 Next Steps
- Add CI/CD pipelines (GitHub Actions / Azure DevOps).  
- Improve observability and alerting in Airflow.  
- Explore data catalogs and lineage for enterprise governance.  

---

#️⃣ Tags  
`#DataEngineering` `#Airflow` `#Snowflake` `#Kafka` `#PySpark` `#GreatExpectations` `#ETL` `#Governance` `#dbt` `#Cloud`
