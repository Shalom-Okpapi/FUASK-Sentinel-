import asyncio
import os
import traceback
from datetime import datetime
from aiogram import Bot

try:
    from monitor import WebsiteMonitor
    from notifier import Notifier
    from settings import PAGES_TO_MONITOR
except ImportError as e:
    print(f"Import Error: {e}")
    print("Make sure all files are in the root directory.")
    exit(1)

async def main():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    bot = Bot(token=bot_token) if bot_token else None

    try:
        print(f"🛡️ FUASK Sentinel Security Check Started - {datetime.now()}")
        
        monitor = WebsiteMonitor()
        results = []
        critical_issues = []
        
        for page in PAGES_TO_MONITOR:
            try:
                result = monitor.check_page(page)
                results.append(result)
                
                if result.get("status_code") != 200 or result.get("anomalies"):
                    critical_issues.append(result)
            except Exception as e:
                error_result = {
                    "name": page["name"],
                    "url": page["url"],
                    "status_code": "Error",
                    "error": str(e)
                }
                results.append(error_result)
                critical_issues.append(error_result)
        
        # Send summary
        if bot and chat_id:
            summary = Notifier.format_daily_report(results)
            await bot.send_message(chat_id, summary)
            
            for issue in critical_issues:
                alert = Notifier.format_security_alert(issue)
                await bot.send_message(chat_id, alert)
        else:
            print("Warning: Telegram credentials not found. Printing to console only.")
            print(Notifier.format_daily_report(results))
        
        print("✅ Check completed successfully.")

    except Exception as e:
        error_msg = f"🚨 Sentinel Crashed!\n\nError: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        
        if bot and chat_id:
            await bot.send_message(chat_id, error_msg[:2000])  # Limit message size

if __name__ == "__main__":
    asyncio.run(main())
