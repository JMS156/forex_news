from requests_html import HTMLSession

session = HTMLSession()
url = "https://www.investing.com/economic-calendar/"
headers = {"User-Agent": "Mozilla/5.0"}

# Render the page with JS
r = session.get(url, headers=headers)
r.html.render(timeout=20)

print("\n📅 ECONOMIC EVENTS (today):\n")
rows = r.html.find('tr.js-event-item')

for row in rows:
    try:
        time = row.find(".first.left.time", first=True).text
        currency = row.find(".left.flagCur.noWrap span", first=True).text
        title = row.find(".event", first=True).text
        impact = row.find(".sentiment span", first=True).attrs.get("title", "")
        print(f"{time} | {currency} | {title} | Impact: {impact}")
    except:
        continue

