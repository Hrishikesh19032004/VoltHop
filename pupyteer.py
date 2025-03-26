import asyncio
from pyppeteer import launch

async def get_tesla_page_source():
    browser = await launch(headless=True, executablePath="C:/path/to/chrome.exe")
    page = await browser.newPage()
    await page.goto("https://www.tesla.com/inventory", {"waitUntil": "networkidle2"})
    content = await page.content()
    await browser.close()

    with open("tesla.html", "w", encoding="utf-8") as file:
        file.write(content)
    print("Page source saved.")

asyncio.run(get_tesla_page_source())

