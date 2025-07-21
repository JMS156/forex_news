import asyncio
from playwright.async_api import async_playwright

async def main():
    print("\n📡 Launching browser...\n")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.forexfactory.com/calendar?day=today")
        await page.wait_for_timeout(10000)  # Increased wait time

        print("📰 FOREX FACTORY NEWS TODAY:\n")

        rows = await page.query_selector_all("tr.calendar__row")
        print(f"Found {len(rows)} events today.\n")

        for row in rows:
            time = await row.query_selector(".calendar__time")
            currency = await row.query_selector(".calendar__currency")
            title = await row.query_selector(".calendar__event-title")
            impact = await row.query_selector(".impact--high, .impact--medium, .impact--low")

            time_text = await time.inner_text() if time else ""
            currency_text = await currency.inner_text() if currency else ""
            title_text = await title.inner_text() if title else ""
            impact_title = await impact.get_attribute("title") if impact else "None"

            print(f"[{impact_title}] {time_text} - {currency_text} - {title_text}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

