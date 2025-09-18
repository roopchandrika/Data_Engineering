import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=3)
}

def fetch_api_to_postgres():
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    users = response.json()
    conn = psycopg2.connect("dbname=airflow user=airflow password=airflow host=postgres")
    cur = conn.cursor()
    for user in users:
        cur.execute("INSERT INTO api_users (id, name, email) VALUES (%s, %s, %s)",
                    (user['id'], user['name'], user['email']))
    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id='api_to_postgres_dag',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2025, 9, 18),
    catchup=False
) as dag:
    task1 = PythonOperator(
        task_id='fetch_api',
        python_callable=fetch_api_to_postgres
    )
