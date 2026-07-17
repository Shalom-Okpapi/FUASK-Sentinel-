import asyncio
import os
import traceback
from datetime import datetime
from aiogram import Bot

from monitor import WebsiteMonitor
from notifier import Notifier
from settings import PAGES_TO_MONITOR
from visual_monitor import VisualMonitor

async def main():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    bot = Bot(token=bot_token) if bot_token else None

    try:
        print(f"🛡️ FUASK Sentinel Advanced Security Check - {datetime.now()}")
        
        monitor = WebsiteMonitor()
        results = []
        critical_issues = []
        
        for page in PAGES_TO_MONITOR:
            try:
                result = monitor.check_page(page)
                results.append(result)
                
                # Take screenshot on problems
                if result.get("status_code") != 200 or result.get("anomalies"):
                    screenshot_path = await VisualMonitor.capture_screenshot(
                        page["url"], page["name"], "error"
                    )
                    if screenshot_path and bot and chat_id:
                        await bot.send_photo(chat_id, open(screenshot_path, 'rb'), caption=Notifier.format_security_alert(result))
                    else:
                        critical_issues.append(result)
                
            except Exception as e:
                error_result = {"name": page["name"], "url": page["url"], "status_code": "Error", "error": str(e)}
                results.append(error_result)
                critical_issues.append(error_result)

        # Send summary report
        if bot and chat_id:
            summary = Notifier.format_daily_report(results)
            await bot.send_message(chat_id, summary)
        
        print("✅ Advanced security check completed.")

    except Exception as e:
        error_msg = f"🚨 Sentinel System Error\n\n{str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        if bot and chat_id:
            await bot.send_message(chat_id, error_msg[:2000])

if __name__ == "__main__":
    asyncio.run(main())
