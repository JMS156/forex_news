import requests
from bs4 import BeautifulSoup

url = "https://www.investing.com/economic-calendar/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "lxml")

# Extract all events
print("\n📅 ECONOMIC EVENTS (today):\n")
for row in soup.select("tr.js-event-item"):
    try:
        time = row.select_one(".first.left.time").text.strip()
        currency = row.select_one(".left.flagCur.noWrap span").text.strip()
        title = row.select_one(".event").text.strip()
        impact = row.select_one(".sentiment span").get("title").strip()

        print(f"{time} | {currency} | {title} | Impact: {impact}")
    except Exception:
        continue

