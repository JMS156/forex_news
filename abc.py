import requests
import pandas as pd

url = "https://www.investing.com/economic-calendar/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Step 1: Download the HTML manually
response = requests.get(url, headers=headers)

# Step 2: Use pandas to parse tables from response.content
tables = pd.read_html(response.content)

print("\n📅 TODAY'S ECONOMIC EVENTS (First 25 Rows):\n")
print(tables[0].head(25))

