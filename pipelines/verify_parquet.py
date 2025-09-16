from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("VerifyParquet").getOrCreate()

df = spark.read.parquet(r"C:\Users\mrcha\Desktop\docker\ELT\data\output\users_by_country")

print("\nPreview of data read from Parquet:\n")
df.show()

spark.stop()
