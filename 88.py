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

        # This selector excludes day-breakers by checking for event column content
        await page.wait_for_selector("tr.calendar__row--grey td.event, tr.calendar__row--white td.event", timeout=30000)

        rows = await page.query_selector_all("tr.calendar__row--grey, tr.calendar__row--white")

        if not rows:
            print("❌ No events found. Try again later.")
            await browser.close()
            return

        print("📰 FOREX FACTORY NEWS TODAY:\n")

        for row in rows:
            try:
                time = await row.query_selector_eval("td.time", "el => el.textContent.trim()")
                currency = await row.query_selector_eval("td.currency", "el => el.textContent.trim()")
                impact = await row.query_selector_eval("td.impact span", "el => el.title")  # e.g. High Impact
                event = await row.query_selector_eval("td.event", "el => el.textContent.trim()")

                if event:  # Skip if no event text
                    print(f"{time} | {currency} | {impact} | {event}")
            except:
                continue

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

