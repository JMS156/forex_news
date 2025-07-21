import asyncio
from playwright.async_api import async_playwright

async def main():
    print("\n📡 Launching browser...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.forexfactory.com/calendar?day=today", timeout=60000)

        print("\n⏳ Waiting for events to load...")
        await page.wait_for_selector("tr.calendar__row", timeout=15000)
        rows = await page.query_selector_all("tr.calendar__row")

        print("\n📰 FOREX FACTORY NEWS TODAY:\n")

        if not rows:
            print("❌ No events found.")
        else:
            for row in rows:
                time = await row.query_selector_eval("td.time", "el => el.innerText").catch(lambda _: "")
                currency = await row.query_selector_eval("td.currency", "el => el.innerText").catch(lambda _: "")
                impact = await row.query_selector_eval("td.impact span", "el => el.getAttribute('title')").catch(lambda _: "")
                event = await row.query_selector_eval("td.event", "el => el.innerText").catch(lambda _: "")

                print(f"🕒 {time.strip()} | 💰 {currency.strip()} | ⚡ {impact.strip()} | 📌 {event.strip()}")

        await browser.close()

asyncio.run(main())

