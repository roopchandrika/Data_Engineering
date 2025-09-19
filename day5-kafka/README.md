
---

# Real-Time Streaming with Kafka, Spark & Delta Lake

## 📌 Project Overview

This project demonstrates a **real-time data pipeline**:

* **Kafka Producer** sends transaction events.
* **Kafka Consumer** verifies events in the `transactions` topic.
* **Spark Structured Streaming** consumes data from Kafka.
* Data is written both to **console (debug)** and **Delta Lake**.
* Delta tables are queried back in **PySpark** for analysis.

---

## ⚙️ Versions Used

* **OS:** Windows 10
* **Python:** 3.13.7 (`py --version`)
* **Apache Spark:** 3.5.1 (`spark-submit --version`)
* **Scala:** 2.12.18 (bundled with Spark)
* **Java:** OpenJDK 17.0.12
* **Kafka:** (local broker on `localhost:9092`)
* **Delta Lake:** `io.delta:delta-spark_2.12:3.2.0`

---

## 📂 Project Structure

```
day5-kafka/
│
├── producer.py             # Kafka Producer
├── consumer.py             # Kafka Consumer
├── spark/
│   └── spark_streaming.py  # Spark Streaming job
├── delta/                  # Delta Lake output
│   └── transactions/       # Data & _delta_log
└── chk/                    # Checkpoint directory
```

---

## 🐍 Python Setup

Install the required packages:

```bash
pip install kafka-python
pip install delta-spark==3.2.0
```

Check installations:

```bash
python -m kafka --version   # should work after kafka-python install
python -c "import delta; print(delta.__version__)"  # should print 3.2.0
```

---

## 🚀 Steps & Commands

### 1️⃣ Kafka Setup

Start Zookeeper and Kafka broker.

```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka broker
bin/kafka-server-start.sh config/server.properties

# Create topic
bin/kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

Run producer:

```bash
python producer.py
```

Run consumer:

```bash
python consumer.py
```

---

### 2️⃣ Spark Streaming (Console Sink)

Run streaming job with console output:

```bash
spark-submit ^
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 ^
  spark\spark_streaming.py
```

---

### 3️⃣ Spark Streaming (Delta Sink)

Run streaming job with Delta sink:

```bash
spark-submit ^
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,io.delta:delta-spark_2.12:3.2.0 ^
  --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension ^
  --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog ^
  spark\spark_streaming.py delta
```

This creates the folder:

```
delta/transactions/
   ├── part-0000…snappy.parquet
   └── _delta_log/
```

---

### 4️⃣ Query Delta Table in PySpark

Launch PySpark with Delta support:

```bash
pyspark --packages io.delta:delta-spark_2.12:3.2.0 ^
  --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension ^
  --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog
```

Read and query data:

```python
df = spark.read.format("delta").load("delta/transactions")
df.show()
```

---

## 🛠️ Troubleshooting Fixed

* **`Module not found: delta-core`** → switched to `delta-spark_2.12:3.2.0`.
* **`python3 not found`** → mapped to `py` on Windows.
* **`StructType.toAttributes()` error** → resolved by aligning Spark 3.5.1 with Delta 3.2.0.
* **Delta configs missing** → added:

  ```bash
  --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension
  --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog
  ```

---

## ✅ Final Result

You now have a working **real-time ETL pipeline**:

```
Kafka Producer → Kafka Topic → Spark Structured Streaming → Delta Lake → Query in PySpark
```

---