import os
from pyspark.sql import SparkSession

# ✅ Force Spark to use Java 17 (Zulu)
os.environ["JAVA_HOME"] = r"C:\Program Files\Zulu\zulu-17"
os.environ["PATH"] = os.environ["JAVA_HOME"] + r"\bin;" + os.environ["PATH"]

# ✅ Create Spark session in local mode (no Hadoop needed)
spark = SparkSession.builder \
    .appName("CSV to Parquet ETL") \
    .master("local[*]") \
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem") \
    .getOrCreate()

# Input CSV (absolute path)
csv_path = r"C:\Users\mrcha\Desktop\docker\ELT\data\users.csv"

# 1. Extract
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# 2. Transform (example: count users by nationality)
agg_df = df.groupBy("nat").count()

# 3. Load → Parquet output
output_path = r"C:\Users\mrcha\Desktop\docker\ELT\data\output\users_by_country"
agg_df.write.mode("overwrite").parquet(output_path)

# ✅ Verification
print("\nParquet write complete! Preview of results:\n")
result = spark.read.parquet(output_path)
result.show()

# 4. Close
spark.stop()
