from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

transactions = ["purchase", "refund", "withdrawal", "deposit"]

while True:
    event = {
        "user_id": random.randint(1, 100),
        "transaction_type": random.choice(transactions),
        "amount": round(random.uniform(10.0, 500.0), 2)
    }
    producer.send("transactions", event)
    print("Produced:", event)
    time.sleep(2)
