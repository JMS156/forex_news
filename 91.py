import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, UTC

async def main():
    print("\n📡 Launching browser...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        today = datetime.now(UTC).strftime("%b%d.%Y").lower()
        url = f"https://www.forexfactory.com/calendar?day={today}"
        await page.goto(url, timeout=60000)

        print("⏳ Waiting and scrolling to load events...\n")
        await asyncio.sleep(8)
        await page.mouse.wheel(0, 5000)
        await asyncio.sleep(4)

        # Get all rows
        rows = await page.query_selector_all("tr.calendar__row")

        print("📰 FOREX FACTORY NEWS TODAY:\n")
        count = 0

        for row in rows:
            # Skip row if it's a 'day-breaker' or empty
            classes = await row.get_attribute("class") or ""
            if "day-breaker" in classes or "spacer" in classes:
                continue

            try:
                time = (await row.query_selector("td.time")).inner_text()
                currency = (await row.query_selector("td.currency")).inner_text()
                impact_elem = await row.query_selector("td.impact span")
                impact = await impact_elem.get_attribute("title") if impact_elem else "N/A"
                event = (await row.query_selector("td.event")).inner_text()

                print(f"{time: <7} | {currency: <5} | {impact: <15} | {event}")
                count += 1
            except:
                continue  # Skip rows with missing fields

        if count == 0:
            print("❌ Still no proper news rows found. May be IP/Captcha issue.\n")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

