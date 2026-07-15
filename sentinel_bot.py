from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from .settings import BOT_TOKEN, CHAT_ID
from .monitor import WebsiteMonitor
from .notifier import Notifier

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

monitor = WebsiteMonitor()

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer("🔍 Running full security scan...")
    results = []
    for page in PAGES_TO_MONITOR:  # Import from settings
        result = monitor.check_page(page)
        results.append(result)
        await message.answer(Notifier.format_security_alert(result))
    
    await message.answer(Notifier.format_daily_report(results))

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🛡️ *FUASK Sentinel* is active!\n\n"
        "Commands:\n"
        "/status - Full security check\n"
        "/report - Daily summary"
    )

async def scheduled_check():
    while True:
        try:
            results = []
            for page in PAGES_TO_MONITOR:
                result = monitor.check_page(page)
                results.append(result)
                
                # Only alert on critical issues
                if result.get("status_code") != 200 or result.get("anomalies"):
                    alert = Notifier.format_security_alert(result)
                    await bot.send_message(CHAT_ID, alert)
            
            # Send daily report once per day (you can improve scheduling later)
            if len(results) > 0:
                await bot.send_message(CHAT_ID, Notifier.format_daily_report(results))
                
        except Exception as e:
            await bot.send_message(CHAT_ID, f"⚠️ Sentinel Error: {e}")
        
        await asyncio.sleep(CHECK_INTERVAL_MINUTES * 60)  # from settings
