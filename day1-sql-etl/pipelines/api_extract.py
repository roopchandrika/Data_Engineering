import requests
import pandas as pd
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

url = "https://randomuser.me/api/?results=50"
data = requests.get(url).json()

df = pd.json_normalize(data["results"])
df.to_csv("data/users.csv", index=False)

logging.info("Extracted 50 users and saved as users.csv")