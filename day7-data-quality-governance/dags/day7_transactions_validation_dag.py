from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

# Function to run GE script inside container
def run_gx_validation():
    # Call your GE script directly
    result = subprocess.run(
        ["python", "/opt/airflow/gx_scripts/day7_gx_script.py"],
        capture_output=True,
        text=True
    )
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    if result.returncode != 0:
        raise Exception("GE validation failed")

# DAG Definition
with DAG(
    dag_id="day7_transactions_validation",
    start_date=datetime(2025, 9, 25),
    schedule_interval="@daily",
    catchup=False,
    tags=["great_expectations", "data_quality"],
) as dag:

    validate_transactions = PythonOperator(
        task_id="validate_transactions",
        python_callable=run_gx_validation,
    )

    validate_transactions
