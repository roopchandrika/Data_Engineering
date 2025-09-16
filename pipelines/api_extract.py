import requests
import pandas as pd
import os

# Make sure output folder exists
os.makedirs("data", exist_ok=True)

# Call Random User API (50 users)
url = "https://randomuser.me/api/?results=50"
resp = requests.get(url)
data = resp.json()["results"]

# Flatten JSON into DataFrame
df = pd.json_normalize(data)

# Save as CSV
csv_path = "data/users.csv"
df.to_csv(csv_path, index=False)

print(f"Extracted {len(df)} users -> saved as {csv_path}")
