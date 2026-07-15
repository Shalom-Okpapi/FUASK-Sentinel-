from playwright.async_api import async_playwright
import asyncio
from datetime import datetime
import os

class VisualMonitor:
    async def capture_screenshot(self, url, name):
        """Capture screenshot of page"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"data/screenshots/{name}_{timestamp}.png"
                
                os.makedirs("data/screenshots", exist_ok=True)
                await page.screenshot(path=filename, full_page=True)
                
                await browser.close()
                return filename
                
        except Exception as e:
            print(f"Screenshot failed for {name}: {e}")
            return None
