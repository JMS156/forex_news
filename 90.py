import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, UTC

async def main():
    print("\n📡 Launching browser...\n")

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()

        today = datetime.now(UTC).strftime("%b%d.%Y").lower()
        url = f"https://www.forexfactory.com/calendar?day={today}"
        await page.goto(url, timeout=60000)

        print("⏳ Waiting and scrolling to load events...\n")
        await page.mouse.wheel(0, 3000)
        await asyncio.sleep(5)

        rows = await page.query_selector_all("tr.calendar__row")

        print("📰 FOREX FACTORY NEWS TODAY:\n")

        count = 0
        for row in rows:
            event_td = await row.query_selector("td.event")
            time_td = await row.query_selector("td.time")
            currency_td = await row.query_selector("td.currency")
            impact_span = await row.query_selector("td.impact span")

            if event_td and time_td and currency_td:
                event = (await event_td.text_content()).strip()
                time = (await time_td.text_content()).strip()
                currency = (await currency_td.text_content()).strip()
                impact = await impact_span.get_attribute("title") if impact_span else "N/A"
                print(f"{time: <7} | {currency: <5} | {impact: <15} | {event}")
                count += 1

        if count == 0:
            print("❌ No usable event rows found.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

