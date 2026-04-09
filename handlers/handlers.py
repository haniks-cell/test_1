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
    
    await message.answer(f'Привет, Выберите цель\nid={message.from_user.id}', reply_markup=startkb)
    

@router.message(F.text == 'main')
async def first (message: types.Message):
    await message.answer('main', reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data == 'ress')
async def ress (callback: types.CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('main', reply_markup=await create_inline(["main", "frst", "scn"]))