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

from aiogram import Bot, Dispatcher, F, Router, types

from aiogram.client.session.aiohttp import AiohttpSession

logging.basicConfig(level=logging.INFO)

proxy_url = "http://127.0.0.1:10808"
session = AiohttpSession(proxy=proxy_url)

bot = Bot(token=settings.SECRET_KEY, session=session)
# Диспетчер
dp = Dispatcher()
dp.message.filter(ChatFilter(['private']), AdminFilter())

async def on_startup(bot):
    await create_db()

# @router.message(Command("eq"))
# async def home (message: types.Message):
#     await bot.send_message(message.from_user.id, '.')
#     print('jfrjrjfj')
#     # await message.answer(f'Привет, Выберите цель\nid={message.from_user.id}', reply_markup=startkb)
    

async def main():
    dp.include_router(router)
    dp.include_router(br)
    dp.startup.register(on_startup)
    # await create_db()
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())