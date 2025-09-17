````
# Day 3 — Data Modeling & Warehousing (dbt + Snowflake)

This project demonstrates how to build a **star-schema style warehouse** in Snowflake using **dbt**.  
I ingested raw CSVs into the `RAW` schema, transform them into staging views, apply a Slowly Changing Dimension (SCD2) snapshot, and build marts (facts and dimensions) in the `ANALYTICS` schema.

---

## 📂 Project Structure
```
dbt\_project/
│── dbt\_project.yml
│── profiles.yml
│── models/
│   ├── sources.yml
│   ├── staging/
│   │   ├── stg\_customers.sql
│   │   ├── stg\_products.sql
│   │   └── stg\_orders.sql
│   └── marts/
│       ├── dim\_customers.sql
│       ├── dim\_products.sql
│       ├── fact\_orders.sql
│       └── sales\_summary.sql
│── snapshots/
│   └── customers\_snapshot.sql
│── tests/

````
---

## ⚙️ Configuration

- **profiles.yml** → stores Snowflake credentials (user, password, account, etc.)
- **dbt_project.yml** → defines models, snapshots, schema overrides

---

## 🔗 Schemas

- `RAW` → raw staging tables (`*_STAGE`)
- `ANALYTICS` → dbt-managed schema (staging views, snapshots, marts)

---

## 🛠️ Workflow

1. **Staging (bronze layer)**  
   Reads from `RAW` sources and creates cleaned views:
   - `stg_customers`
   - `stg_products`
   - `stg_orders`

2. **Snapshots (SCD2)**  
   Tracks changes in customer attributes (`customers_snapshot`) using dbt snapshots.

3. **Marts (silver/gold layer)**  
   - `dim_customers` → current customer dimension (from snapshot)  
   - `dim_products` → product dimension  
   - `fact_orders` → fact table combining orders + products  
   - `sales_summary` → aggregate view by country, category, and day  

---

## 🚀 Run Commands

```bash
# Clean cache
dbt clean

# Run staging views
dbt run --select staging

# Apply snapshots (SCD2)
dbt snapshot

# Run marts
dbt run --select marts

# Run all tests
dbt test
````

---

## ✅ Expected Outputs

In the `ANALYTICS` schema:

* `stg_customers`, `stg_products`, `stg_orders` (views)
* `customers_snapshot` (SCD2 table)
* `dim_customers`, `dim_products` (dimension tables)
* `fact_orders` (fact table)
* `sales_summary` (aggregated summary view)

```

---
<img width="1589" height="1044" alt="output" src="https://github.com/user-attachments/assets/4050f2d6-3e5c-44ad-b060-850decbe83f1" />



