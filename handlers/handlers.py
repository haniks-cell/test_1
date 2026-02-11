import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from database.models import Group, Question
from keybords.keyboards import repkeyb, inlkeyb, create_inline, startkb

from filters.main_filter import ChatFilter, AdminFilter

router = Router()

@router.message(CommandStart())
async def home (message: types.Message, session: AsyncSession):
    # if message.from_user.id not in access_usr:
    #     return
    # session.add(Question(idname=1, body='two' ))
    # query = select(Group).options(joinedload(Group.quest))
    # res = await session.execute(query)
    # # await session.commit()
    # result = res.unique().scalars().all()
    # print(result[0].quest[1].body)
    # print(await session.scalars(query))
    # await message.answer('Привет', reply_markup=await create_inline(["main", "frst", "scn"]))
    await message.answer(f'Привет, Выберите цель\nid={message.from_user.id}', reply_markup=startkb)
    # await message.answer(f'Привет, Выберите цель\nid={res.unique().scalars().all()}', reply_markup=startkb)

@router.message(F.text == 'main')
async def first (message: types.Message):
    await message.answer('main', reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data == 'ress')
async def ress (callback: types.CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('main', reply_markup=await create_inline(["main", "frst", "scn"]))