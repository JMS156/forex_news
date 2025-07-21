import asyncio
from playwright.async_api import async_playwright

async def main():
    print("\n📡 Launching browser...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.forexfactory.com/calendar?day=today", timeout=60000)

        print("\n⏳ Waiting and scrolling to load events...")

        # Scroll multiple times
        for _ in range(3):
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(2)

        # Wait for at least one row to appear
        try:
            await page.wait_for_selector("tr.calendar__row", timeout=15000)
        except:
            print("❌ News rows not found (timeout). Try again shortly.")
            await browser.close()
            return

        print("\n📰 FOREX FACTORY NEWS TODAY:\n")

        rows = await page.query_selector_all("tr.calendar__row")
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

