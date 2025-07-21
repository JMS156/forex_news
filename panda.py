import pandas as pd

url = "https://www.investing.com/economic-calendar/"
headers = {"User-Agent": "Mozilla/5.0"}

# Read all HTML tables from the page
tables = pd.read_html(url)

print("\n📅 TODAY'S ECONOMIC EVENTS (RAW TABLE):\n")
print(tables[0].head(25))  # Show first 25 rows

