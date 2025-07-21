import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, UTC

async def main():
    print("\n📡 Launching browser...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Load today's news
        today = datetime.now(UTC).strftime("%b%d.%Y").lower()
        url = f"https://www.forexfactory.com/calendar?day={today}"
        await page.goto(url, timeout=60000)

        print("⏳ Waiting and scrolling to load events...\n")
        await asyncio.sleep(7)
        await page.mouse.wheel(0, 6000)
        await asyncio.sleep(3)

        # Get only usable rows
        rows = await page.query_selector_all("tr.calendar__row")
        print("📰 FOREX FACTORY NEWS TODAY:\n")

        count = 0
        for row in rows:
            # Skip if it's not a usable event row (has no impact or time)
            impact_elem = await row.query_selector("td.impact span")
            if not impact_elem:
                continue

            try:
                time = (await row.query_selector("td.time")).inner_text()
                currency = (await row.query_selector("td.currency")).inner_text()
                impact = await impact_elem.get_attribute("title")
                event = (await row.query_selector("td.event")).inner_text()

                print(f"{time: <7} | {currency: <5} | {impact: <15} | {event}")
                count += 1
            except:
                continue

        if count == 0:
            print("❌ Still no proper news rows found. Try again later.\n")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

