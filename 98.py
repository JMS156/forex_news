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

        await page.wait_for_selector("tr.calendar__row", timeout=30000)
        rows = await page.query_selector_all("tr.calendar__row")

        print("📰 FOREX FACTORY NEWS TODAY:\n")

        if not rows:
            print("❌ No events found.")
            return

        for row in rows:
            try:
                time = await row.query_selector_eval("td.time", "el => el.textContent.trim()")
                currency = await row.query_selector_eval("td.currency", "el => el.textContent.trim()")
                impact = await row.query_selector_eval("td.impact span", "el => el.title")
                event = await row.query_selector_eval("td.event", "el => el.textContent.trim()")

                if event:  # Only print rows with event names
                    print(f"{time} | {currency} | {impact} | {event}")

            except Exception as e:
                # Debug: uncomment below to print why any row fails
                # print(f"⚠️ Row skipped due to error: {e}")
                continue

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

