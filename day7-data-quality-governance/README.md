---

# 📘 Day 7 – Data Quality & Governance

This project integrates **Great Expectations (GX)** with **Apache Airflow** (running in Docker) to perform automated data quality checks on `transactions.csv`.

---

## 🛠️ Environment Setup

* **Docker Compose services**:

  * `postgres` → Airflow metadata DB.
  * `airflow-init` → initializes DB & user.
  * `airflow-webserver` → Airflow UI (`http://localhost:8081`).
  * `airflow-scheduler` → runs DAGs.

* **FERNET Key** (for secure Airflow connections):

  ```bash
  openssl rand -base64 32
  ```

  Use the generated key in `AIRFLOW__CORE__FERNET_KEY` inside `docker-compose.yml`.

---

## 📂 Folder Structure

```
day7-data-quality-governance/
│
├── dags/
│   └── day7_transactions_validation_dag.py   # Airflow DAG
│
├── gx_scripts/
│   └── day7_gx_script.py                     # GX validation script
│
├── great_expectations/                       # GX configs (suites, checkpoints, etc.)
│
├── transactions.csv                          # Input dataset for validation
│
└── docker-compose.yml                        # Defines Airflow + Postgres services
```

---

## ⚙️ What Was Implemented

1. **Great Expectations Script (`gx_scripts/day7_gx_script.py`)**

   * Loads GX context from `/opt/airflow/great_expectations`.
   * Datasource: local CSV (`transactions.csv`).
   * Expectations applied:

     * `user_id` → must not be null.
     * `transaction_type` → must be `CREDIT` or `DEBIT`.
     * `amount` → must be between `0` and `10,000`.
   * Creates Expectation Suite → `transactions_suite`.
   * Defines Checkpoint → `transactions_checkpoint`.
   * Runs validation and prints results.

2. **Airflow DAG (`dags/day7_transactions_validation_dag.py`)**

   * DAG ID: `day7_transactions_validation`.
   * Schedule: `@daily`.
   * Uses **PythonOperator** to run `day7_gx_script.py`.
   * Fails DAG run if GX validation fails.

---

## ▶️ How to Run

1. Start containers:

   ```bash
   docker-compose up --build -d
   ```

2. Check running containers:

   ```bash
   docker ps
   ```

3. Access Airflow UI:
   👉 [http://localhost:8081](http://localhost:8081)
   Username: `admin`
   Password: `admin`

4. Trigger DAG → `day7_transactions_validation`.

5. View task logs → GX validation results appear in console.

---

## ✅ Expected Output

* If dataset passes validation →

  ```
  Checkpoint executed successfully.
  ```

* If dataset fails validation →
  Errors logged in Airflow and Data Docs (inside `great_expectations/`).

---

## 🐞 Troubleshooting

* **FERNET key error** → regenerate with

  ```bash
  openssl rand -base64 32
  ```

  and update `docker-compose.yml`.

* **Module not found (`great_expectations`)** → install inside container:

  ```bash
  docker exec -it <airflow-container> pip install great_expectations
  ```

* **Path issues** → ensure volumes are mounted correctly in `docker-compose.yml`:

  ```yaml
  - ./transactions.csv:/opt/airflow/data/transactions.csv
  - ./gx_scripts:/opt/airflow/gx_scripts
  - ./great_expectations:/opt/airflow/great_expectations
  ```

---