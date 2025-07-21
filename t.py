import asyncio
from playwright.async_api import async_playwright

async def main():
    print("\n📡 Launching browser...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.forexfactory.com/calendar?day=today", timeout=60000)
        await page.wait_for_timeout(10000)

        content = await page.content()
        with open("page_dump.html", "w", encoding="utf-8") as f:
            f.write(content)

        print("\n✅ Page content saved to 'page_dump.html'")

        await browser.close()

asyncio.run(main())

