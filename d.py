import asyncio
from playwright.async_api import async_playwright

async def main():
    print("\n📡 Launching browser...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "https://www.forexfactory.com/calendar"
        await page.goto(url)
        await page.wait_for_timeout(6000)

        rows = await page.query_selector_all("tr.calendar__row")

        print("\n📰 FOREX FACTORY NEWS TODAY:\n")
        for row in rows:
            try:
                time = await row.query_selector(".calendar__time")
                currency = await row.query_selector(".calendar__currency")
                title = await row.query_selector(".calendar__event-title")
                impact = await row.query_selector(".impact")

                time_text = await time.inner_text() if time else "-"
                currency_text = await currency.inner_text() if currency else "-"
                title_text = await title.inner_text() if title else "-"
                impact_title = await impact.get_attribute("title") if impact else "-"

                print(f"{time_text:>6} | {currency_text:<3} | {title_text:<40} | Impact: {impact_title}")
            except:
                continue

        await browser.close()

asyncio.run(main())

