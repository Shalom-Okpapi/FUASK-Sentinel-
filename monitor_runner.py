import asyncio
import os
from datetime import datetime
from aiogram import Bot
from monitor import WebsiteMonitor
from notifier import Notifier
from settings import PAGES_TO_MONITOR

async def main():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return

    bot = Bot(token=bot_token)
    monitor = WebsiteMonitor()
    
    print(f"🛡️ Starting FUASK Sentinel Security Check - {datetime.now()}")
    
    results = []
    critical_issues = []
    
    for page in PAGES_TO_MONITOR:
        result = monitor.check_page(page)
        results.append(result)
        
        # Collect critical issues for alert
        if result.get("status_code") != 200 or result.get("anomalies"):
            critical_issues.append(result)
    
    # Send summary
    summary = Notifier.format_daily_report(results)
    await bot.send_message(chat_id, summary)
    
    # Send individual critical alerts
    for issue in critical_issues:
        alert = Notifier.format_security_alert(issue)
        await bot.send_message(chat_id, alert)
    
    print("✅ Check completed and notifications sent.")

if __name__ == "__main__":
    asyncio.run(main())
