from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='postgres_to_dbt_dag',
    default_args=default_args,
    description='Run dbt transformations after Postgres load',
    schedule_interval='@daily',
    start_date=datetime(2025, 9, 18),
    catchup=False
) as dag:

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd /opt/airflow/dags/dbt_project && dbt run"
    )
