import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

async def main():
    print("\n📡 Launching browser...\n")

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()

        today = datetime.utcnow().strftime("%b%d.%Y").lower()
        url = f"https://www.forexfactory.com/calendar?day={today}"
        await page.goto(url, timeout=60000)

        print("⏳ Waiting and scrolling to load events...\n")

        # Scroll a bit to force render
        await page.mouse.wheel(0, 2000)
        await asyncio.sleep(3)

        # Force re-check
        rows = await page.query_selector_all("tr.calendar__row")

        print("📰 FOREX FACTORY NEWS TODAY:\n")

        count = 0
        for row in rows:
            try:
                event = await row.query_selector("td.event")
                if event:
                    time = await row.query_selector_eval("td.time", "el => el.textContent.trim()")
                    currency = await row.query_selector_eval("td.currency", "el => el.textContent.trim()")
                    impact_el = await row.query_selector("td.impact span")
                    impact = await impact_el.get_attribute("title") if impact_el else "N/A"
                    event_name = await event.text_content()
                    print(f"{time} | {currency} | {impact} | {event_name.strip()}")
                    count += 1
            except:
                continue

        if count == 0:
            print("❌ No usable event rows found.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

