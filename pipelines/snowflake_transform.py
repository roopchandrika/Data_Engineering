import os
import snowflake.connector
from dotenv import load_dotenv
import sys
sys.stdout.reconfigure(encoding='utf-8')
# Load Snowflake credentials
load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

cur = conn.cursor()

print("Running transformation from STAGE → FINAL...")

# Transformation query
cur.execute("""
    INSERT INTO USERS_BY_COUNTRY_FINAL (NAT, USER_COUNT, LOAD_TIMESTAMP)
    SELECT 
        NAT, 
        COUNT, 
        CURRENT_TIMESTAMP
    FROM USERS_BY_COUNTRY_STAGE
    WHERE NAT IS NOT NULL
""")

print(f"Transformation complete! Rows inserted: {cur.rowcount}")

cur.close()
conn.close()
