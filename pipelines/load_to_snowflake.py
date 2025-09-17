import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

def load_csv(path, table):
    df = pd.read_csv(path)
    success, nchunks, nrows, _ = write_pandas(conn, df, table)
    print(f"[OK] {path} -> {table} rows={nrows} success={success}")

load_csv("data/customers.csv", "CUSTOMERS_STAGE")
load_csv("data/products.csv", "PRODUCTS_STAGE")
load_csv("data/orders.csv", "ORDERS_STAGE")

conn.close()
