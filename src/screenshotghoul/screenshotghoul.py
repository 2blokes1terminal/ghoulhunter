import asyncio


async def take_screenshot(domain, page, output):
    try:
        await asyncio.wait_for(page.goto(f'https://{domain}/', options={'timeout': 5000}), timeout=5)
    except TimeoutError:
        print(f'[screenshotghoul - ERR] timed out')
    await page.screenshot({'path': f'output/{domain}.png'})


def run_take_screenshot(domain, page, output):
    asyncio.get_event_loop().run_until_complete(take_screenshot(domain, page, output))
