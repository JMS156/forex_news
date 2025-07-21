import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

async def main():
    print("\n📡 Launching browser...\n")

    async with async_playwright() as p:
        try:
            browser = await p.firefox.launch(headless=True)  # Use Firefox instead of Chromium
            page = await browser.new_page()
            today = datetime.utcnow().strftime("%b%d.%Y").lower()  # e.g. 'jul21.2025'
            url = f"https://www.forexfactory.com/calendar?day={today}"
            await page.goto(url, timeout=60000)

            print("⏳ Waiting and scrolling to load events...\n")
            await page.wait_for_selector("tr.calendar__row", timeout=20000)

            # Extract all rows
            rows = await page.query_selector_all("tr.calendar__row")
            if not rows:
                print("❌ No events found. Try again shortly.")
                await browser.close()
                return

            print("📰 FOREX FACTORY NEWS TODAY:\n")

            for row in rows:
                time = await row.query_selector_eval("td.time", "el => el.textContent.trim()")
                currency = await row.query_selector_eval("td.currency", "el => el.textContent.trim()")
                impact = await row.query_selector_eval("td.impact span", "el => el.className", strict=False) or "low"
                event = await row.query_selector_eval("td.event", "el => el.textContent.trim()")

                print(f"{time} | {currency} | {impact} | {event}")

            await browser.close()

        except Exception as e:
            print("❌ Error during scraping:", str(e))

if __name__ == "__main__":
    asyncio.run(main())

