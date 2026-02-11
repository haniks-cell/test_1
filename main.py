import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command, CommandObject, CommandStart

from database.engine import create_db, session_maker, drop_db
from middlewares.middlewares import DataBaseSession
from database.config import settings

from handlers.handlers import router
from handlers.br import router as br

from filters.main_filter import ChatFilter, AdminFilter

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=settings.SECRET_KEY)
# Диспетчер
dp = Dispatcher()
dp.message.filter(ChatFilter(['private']), AdminFilter())

async def on_startup(bot):
    await create_db()

async def main():
    dp.include_router(router)
    dp.include_router(br)
    dp.startup.register(on_startup)
    # await create_db()
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())