
# 🚀 Mini ELT Pipeline with PySpark & Snowflake

This project demonstrates a simple **end-to-end ELT pipeline** built with **Python, PySpark, Hadoop (for Windows compatibility), and Snowflake**.  
The pipeline extracts user data from an API, transforms it using Spark, and finally loads it into Snowflake for analytics.

---

## 📂 Project Structure
```

.
├── data/                     # Local data storage
│   ├── users.csv             # Extracted raw CSV
│   ├── output/               # Spark Parquet output
│   └── delta/                # Delta format (optional)
├── pipelines/                # Python ETL pipelines
│   ├── api\_extract.py        # Pipeline 1: API → CSV
│   ├── csv\_to\_parquet.py     # Pipeline 2: CSV → Parquet
│   ├── parquet\_to\_snowflake.py # Pipeline 3: Parquet → Snowflake
│   └── snowflake\_transform.py # Transform STAGE → FINAL
├── .env                      # Snowflake credentials (not committed)
└── README.md                 # Project guide

````

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites
- **Java 17** (Zulu 17 works fine)
- **Apache Spark 3.5.1** with Hadoop 3.x support
- **Hadoop (Windows build)** for `winutils.exe`
- **Python 3.12+**
- **Snowflake account** (with DB, Schema, Warehouse)
- Environment variables stored in `.env`

---

### 2️⃣ Environment Variables (`.env`)
Create a `.env` file in the project root with:

```ini
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account_id.region   # e.g. abc12345.us-east-1
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ETL_DEMO
SNOWFLAKE_SCHEMA=PUBLIC
````

---

### 3️⃣ Pipelines

#### 🔹 Pipeline 1: API → CSV

Fetches **50 random users** from `randomuser.me` and saves them to `data/users.csv`.

```bash
python pipelines/api_extract.py
```

✔️ Output: `data/users.csv`

---

#### 🔹 Pipeline 2: CSV → Parquet

Reads the CSV with PySpark, aggregates user counts by country (`nat`), and writes results to Parquet.

```bash
python pipelines/csv_to_parquet.py
```

✔️ Output: `data/output/users_by_country`

---

#### 🔹 Pipeline 3: Parquet → Snowflake

* Reads the Parquet data
* Writes to a Snowflake staging table (`USERS_BY_COUNTRY_STAGE`)
* Also demonstrates Delta Lake output (optional)

```bash
python pipelines/parquet_to_snowflake.py
```

✔️ Loads data into **Snowflake staging table**

---

#### 🔹 Transformation: Stage → Final

Moves data from **staging** into a **final table** with a load timestamp.

```bash
python pipelines/snowflake_transform.py
```

✔️ Inserts rows into `USERS_BY_COUNTRY_FINAL`

---

## 🛠️ Troubleshooting

* **Java version mismatch** → Ensure Spark and Hadoop run with Java 17 (`where java` to confirm).
* **Hadoop errors on Windows** → Install Hadoop 3.3.x, place `winutils.exe` in `C:\hadoop\bin`, and set `HADOOP_HOME`.
* **Unicode errors in console** → Replace special symbols (✓, →) with ASCII (`->`) or force UTF-8 with `sys.stdout.reconfigure(encoding='utf-8')`.

---

## 📊 Final Outcome

1. Extract user data from API
2. Transform and aggregate with Spark
3. Load into **Snowflake** staging & final tables
4. Data is ready for BI tools (Power BI, Tableau, etc.) 🚀

---

## ✅ Next Steps

* Automate pipelines with **Airflow / Prefect**
* Schedule daily loads
* Add **data quality checks** before Snowflake load
* Expand to multi-table incremental ELT
