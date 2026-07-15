import asyncio
from sentinel_bot import dp, bot, scheduled_check
from settings import CHECK_INTERVAL_MINUTES

async def main():
    print("🛡️ FUASK Sentinel Cybersecurity Bot Started")
    
    # Start scheduled monitoring in background
    asyncio.create_task(scheduled_check())
    
    # Start Telegram bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
