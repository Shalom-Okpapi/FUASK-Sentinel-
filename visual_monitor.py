import os
from datetime import datetime
from playwright.async_api import async_playwright

class VisualMonitor:
    @staticmethod
    async def capture_screenshot(url, name, reason="error"):
        """Take screenshot when there's a problem or change"""
        try:
            os.makedirs("data/screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/screenshots/{name}_{reason}_{timestamp}.png"
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=30000)
                await page.screenshot(path=filename, full_page=True)
                await browser.close()
                
                return filename
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None
