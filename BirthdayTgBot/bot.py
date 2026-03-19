import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers import register_handlers
from scheduler import check_birthdays


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    print("🚀 Бот запущен")
    
    register_handlers(dp)
    
    asyncio.create_task(check_birthdays(bot))
    print("⏰ Планировщик напоминаний запущен")
    
    print("✅ Бот готов к работе")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Бот остановлен")