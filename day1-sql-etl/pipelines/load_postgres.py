import pandas as pd
from sqlalchemy import create_engine

# Read CSV
df = pd.read_csv("data/users.csv")

# Connect to Postgres
engine = create_engine("postgresql://postgres:postgres@127.0.0.1:5433/etl_demo")

# Load into table
df.to_sql("users", engine, if_exists="replace", index=False)

print("✅ Loaded users.csv into Postgres table 'users'")
