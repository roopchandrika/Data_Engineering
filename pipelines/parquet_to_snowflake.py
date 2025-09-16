import os
from pyspark.sql import SparkSession
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# 1. Create Spark session (no Delta needed now)
spark = SparkSession.builder \
    .appName("ParquetToSnowflake") \
    .getOrCreate()

# 2. Define paths
parquet_path = r"C:\Users\mrcha\Desktop\docker\ELT\data\output\users_by_country"

# 3. Read data from Parquet
df = spark.read.parquet(parquet_path)
print("\nData read from Parquet:")
df.show()

# 4. Convert Spark DF → Pandas DF
pdf = df.toPandas()

# 🔑 Fix column names (uppercase for Snowflake compatibility)
pdf.columns = [c.upper() for c in pdf.columns]

# 5. Snowflake connection details (from .env or hardcoded for testing)
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER", "Chandrika"),
    password=os.getenv("SNOWFLAKE_PASSWORD", "Chandrika@0957"),
    account=os.getenv("SNOWFLAKE_ACCOUNT", "fgbubxd-yua59733"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    database=os.getenv("SNOWFLAKE_DATABASE", "ETL_DEMO"),
    schema=os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
)

# 6. Write Pandas DF → Snowflake table
success, nchunks, nrows, _ = write_pandas(
    conn,
    pdf,
    table_name="USERS_BY_COUNTRY_STAGE",   # Table already created
    database="ETL_DEMO",
    schema="PUBLIC"
)

print(f"\nData written to Snowflake table USERS_BY_COUNTRY_STAGE")
print(f"Inserted rows: {nrows}")

# 7. Close connection
conn.close()
spark.stop()
