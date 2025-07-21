import asyncio
from playwright.async_api import async_playwright

async def main():
    print("\n📡 Launching browser...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.forexfactory.com/calendar?day=today", timeout=60000)

        print("⏳ Waiting and scrolling to load events...\n")
        await page.mouse.wheel(0, 3000)
        await asyncio.sleep(3)

        print("📰 FOREX FACTORY NEWS TODAY:\n")

        rows = await page.query_selector_all("tr.calendar__row")
        count = 0

        for row in rows:
            # Don’t filter by class. Just grab whatever we can.
            time_el = await row.query_selector("td.time")
            currency_el = await row.query_selector("td.currency")
            impact_el = await row.query_selector("td.impact span")
            event_el = await row.query_selector("td.event")

            if not all([time_el, currency_el, impact_el, event_el]):
                continue

            time = await time_el.inner_text()
            currency = await currency_el.inner_text()
            impact = await impact_el.get_attribute("title")
            event = await event_el.inner_text()

            print(f"{time: <8} | {currency: <5} | {impact: <15} | {event}")
            count += 1

        if count == 0:
            print("❌ Still no usable event rows found. Captcha/IP block?\n")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

