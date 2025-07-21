import requests
from datetime import datetime

# Setup
url = "https://api.tradingeconomics.com/calendar"
params = {
    "c": "guest:guest",
    "f": "json"
}

response = requests.get(url, params=params)
data = response.json()

# Today’s date in ISO format
today_str = datetime.utcnow().strftime('%Y-%m-%d')

print("\n📅 TODAY'S EVENTS:\n")
found = False

for event in data:
    if event.get("Date", "").startswith(today_str):
        found = True
        time = event['Date'][11:16]
        country = event.get("Country", "")
        name = event.get("Event", "")
        impact = event.get("Importance", "")
        print(f"{time} | {country:15} | {name:50} | Impact: {impact}")

if not found:
    print("No events found for today.")

