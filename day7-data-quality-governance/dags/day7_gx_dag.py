from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def run_gx_validation():
    # Run the GX script
    result = subprocess.run(
        ["python", "/opt/airflow/gx_scripts/day7_gx_script.py"], 
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception("GX validation failed")

with DAG(
    dag_id="day7_transactions_validation",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["day7", "gx", "data-quality"]
) as dag:

    validate = PythonOperator(
        task_id="gx_validate_transactions",
        python_callable=run_gx_validation
    )
