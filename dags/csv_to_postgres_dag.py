from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import psycopg2

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

def load_csv_to_postgres():
    conn = psycopg2.connect("dbname=airflow user=airflow password=airflow host=postgres")
    cur = conn.cursor()
    df = pd.read_csv('/opt/airflow/dags/data/customers.csv')
    for _, row in df.iterrows():
        cur.execute("INSERT INTO customers (id, name, email) VALUES (%s, %s, %s)", (row['id'], row['name'], row['email']))
    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id='csv_to_postgres_dag',
    default_args=default_args,
    description='Load CSV into Postgres',
    schedule_interval='@daily',
    start_date=datetime(2025, 9, 18),
    catchup=False
) as dag:
    task1 = PythonOperator(
        task_id='load_csv',
        python_callable=load_csv_to_postgres
    )
