import asyncio
from playwright.async_api import async_playwright

async def main():
    print("\n📡 Launching browser...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.forexfactory.com/calendar?day=today", timeout=60000)

        print("\n⏳ Waiting and scrolling to load events...")
        await asyncio.sleep(2)
        await page.mouse.wheel(0, 8000)
        await asyncio.sleep(5)

        rows = await page.query_selector_all("tr.calendar__row")
        print("\n📰 FOREX FACTORY NEWS TODAY:\n")

        if not rows:
            print("❌ No events found. Try again after a minute.")
        else:
            for row in rows:
                time = await row.query_selector("td.time")
                currency = await row.query_selector("td.currency")
                impact = await row.query_selector("td.impact span")
                event = await row.query_selector("td.event")

                time_text = await time.inner_text() if time else "-"
                currency_text = await currency.inner_text() if currency else "-"
                impact_text = await impact.get_attribute("title") if impact else "-"
                event_text = await event.inner_text() if event else "-"

                print(f"🕒 {time_text.strip()} | 💰 {currency_text.strip()} | ⚡ {impact_text.strip()} | 📌 {event_text.strip()}")

        await browser.close()

asyncio.run(main())

