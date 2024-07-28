import requests
import pandas as pd
import io

def fetch_data(DATA_URL,HEADERS,DATA_PATH):
    response = requests.get(DATA_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.content.decode('utf-8')
    csv_data = pd.read_csv(io.StringIO(data))
    csv_data.to_excel(DATA_PATH, index=False)
    print(f"Data fetched and saved to {DATA_PATH}")