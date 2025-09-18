---

# 📘 Day 4 – Orchestration with Airflow

## ✅ Overview

On Day 4, I set up **Apache Airflow** locally using **Docker Compose** with a Postgres backend and orchestrated three data pipelines

1. **CSV → Postgres**
2. **API → Postgres**
3. **Postgres → dbt transformations**

This completes the orchestration layer of the data engineering workflow.

---

## 🏗️ Project Structure

```
day4-airflow/
│── docker-compose.yml        # Airflow + Postgres setup
│── dags/
│   ├── csv_to_postgres_dag.py   # Load CSV into Postgres
│   ├── api_to_postgres_dag.py   # Load API data into Postgres
│   ├── postgres_to_dbt_dag.py   # Run dbt models on Postgres
│   └── data/
│       └── customers.csv        # Sample CSV input
│── requirements.txt          # Python dependencies if needed
│── README.md                 # Documentation
```

---

## ⚙️ Setup Instructions

### 1. Start Airflow + Postgres

```bash
docker-compose up -d
```

### 2. Initialize Database (done via `airflow-init` service)

Admin user created automatically:

* **Username**: `airflow`
* **Password**: `airflow`

Access UI at: [http://localhost:8080](http://localhost:8080)

---

### 3. Create Target Tables in Postgres

```bash
docker exec -it elt-postgres-1 psql -U airflow -d airflow
```

Inside psql:

```sql
CREATE TABLE customers (id INT, name TEXT, email TEXT);
CREATE TABLE api_users (id INT, name TEXT, email TEXT);
\q
```

---

### 4. Trigger DAGs

**CSV → Postgres**

```bash
docker exec -it elt-webserver-1 airflow dags trigger csv_to_postgres_dag
```

**API → Postgres**

```bash
docker exec -it elt-webserver-1 airflow dags trigger api_to_postgres_dag
```

**Postgres → dbt (optional)**

```bash
docker exec -it elt-webserver-1 airflow dags trigger postgres_to_dbt_dag
```

---

### 5. Verify Data

Check data inside Postgres:

```bash
docker exec -it elt-postgres-1 psql -U airflow -d airflow -c "SELECT * FROM customers;"
docker exec -it elt-postgres-1 psql -U airflow -d airflow -c "SELECT * FROM api_users;"
```

---

## 📊 Workflow Summary

* **Orchestration Tool**: Apache Airflow (v2.9.1)
* **Metadata DB**: Postgres (instead of default SQLite)
* **Pipelines Built**:

  * ✅ Load CSV file → `customers` table in Postgres
  * ✅ Fetch API data → `api_users` table in Postgres
  * ✅ Trigger dbt models from Airflow (Postgres as source)

---

## 📚 Concepts Learned

* **Airflow DAGs** → definition of workflows
* **Operators & Hooks** → PythonOperator, PostgresHook for inserts
* **Retries & Scheduling** → Airflow handles retries on failure
* **Dockerized Airflow** → running Airflow locally with Postgres backend
* **Integration with dbt** → orchestrating transformations downstream

---

## 🎯 Key Takeaways

* Learned how to orchestrate **end-to-end pipelines** with Airflow.
* Replaced Airflow’s default SQLite with **Postgres metadata DB**.
* Built real DAGs for ingestion (CSV, API) and transformation (dbt).
* Confirmed results in Postgres by querying target tables.

---

