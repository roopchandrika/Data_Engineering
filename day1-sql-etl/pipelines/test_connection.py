from sqlalchemy import create_engine

# Candidate connection strings
connection_strings = [
  
    "postgresql://postgres:postgres@127.0.0.1:5433/etl_demo"
]

for conn_str in connection_strings:
    print(f"🔍 Trying: {conn_str}")
    try:
        engine = create_engine(conn_str)
        conn = engine.connect()
        print(f"✅ SUCCESS: Connected using {conn_str}\n")
        conn.close()
    except Exception as e:
        print(f"❌ FAILED: {conn_str}\n   Error: {e}\n")
