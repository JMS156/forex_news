import requests
from bs4 import BeautifulSoup

url = "https://www.investing.com/economic-calendar/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "lxml")

print("\n📅 ECONOMIC EVENTS:\n")
rows = soup.select("tr.js-event-item")

for row in rows:
    try:
        time = row.select_one(".first.left.time").text.strip()
        currency = row.select_one(".left.flagCur.noWrap span").text.strip()
        title = row.select_one(".event").text.strip()
        impact = row.select_one(".sentiment span")["title"].strip()
        print(f"{time:>7} | {currency:<3} | {title:<40} | Impact: {impact}")
    except Exception:
        continue

