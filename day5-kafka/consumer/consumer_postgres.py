from kafka import KafkaConsumer
import psycopg2, json

# Connect to Postgres
conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="airflow",
    user="airflow",
    password="airflow"
)
cur = conn.cursor()

# Ensure table exists
cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    user_id INT,
    transaction_type TEXT,
    amount NUMERIC
)
""")
conn.commit()

# Kafka Consumer
consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Consumer started...")

for msg in consumer:
    event = msg.value
    print("Consumed:", event)

    cur.execute(
        "INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, %s, %s)",
        (event["user_id"], event["transaction_type"], event["amount"])
    )
    conn.commit()
