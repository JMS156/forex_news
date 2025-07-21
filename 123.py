import requests

url = "https://api.tradingeconomics.com/calendar/country/all"
params = {
    "c": "guest:guest",  # guest credentials
    "f": "json"          # return as JSON
}

response = requests.get(url, params=params)
data = response.json()

print("\n📅 TODAY'S EVENTS:\n")

for event in data:
    if event['Date'][:10] == str(response.headers['Date'])[:10]:  # crude today filter
        print(f"{event['Date'][11:16]} | {event['Country']} | {event['Event']} | Impact: {event['Importance']}")

