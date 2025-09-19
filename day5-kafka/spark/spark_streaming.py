import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, IntegerType

# Choose sink type from command line args (default = console)
# Example: spark-submit ... spark/spark_streaming.py delta
sink = "console"
if len(sys.argv) > 1:
    sink = sys.argv[1].lower()

# Spark session with Delta support
spark = SparkSession.builder \
    .appName("KafkaSparkDelta") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Schema
schema = StructType() \
    .add("user_id", IntegerType()) \
    .add("transaction_type", StringType()) \
    .add("amount", DoubleType())

# Read from Kafka
# Read from Kafka with earliest offset
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse JSON
parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write Stream depending on sink
if sink == "delta":
    query = parsed.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", "chk/") \
        .option("path", "delta/transactions") \
        .start()
    print("Writing to Delta Lake (delta/transactions)")
else:
    query = parsed.writeStream \
        .format("console") \
        .outputMode("append") \
        .start()
    print("Writing to console (debug mode)")

query.awaitTermination()
