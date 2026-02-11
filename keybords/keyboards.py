from typing import Sequence
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from database.models import Group, Question

repkeyb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='main')],
    [KeyboardButton(text='first'), KeyboardButton(text='second')]
], resize_keyboard=True, input_field_placeholder='Select')

inlkeyb = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='test', url="https://www.youtube.com/watch?v=qRyshRUA0xM")],
    [InlineKeyboardButton(text='перевернуть', callback_data='ress'), InlineKeyboardButton(text='perer', callback_data='perer')]
])

startkb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='БР', callback_data='br_start'),InlineKeyboardButton(text='ST', callback_data='st_start'),]
], resize_keyboard=True)

async def create_inline (lis:list) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    bld = InlineKeyboardBuilder()
    for el in lis:
        bld.add(InlineKeyboardButton(text=el, url='https://www.youtube.com/watch?v=qRyshRUA0xM'))
    return bld.adjust(1,2).as_markup()

async def create_reply (lis:Sequence[Group]) -> ReplyKeyboardMarkup:
    bld = ReplyKeyboardBuilder()
    for el in lis:
        bld.add(KeyboardButton(text=el.name))
    return bld.adjust(2).as_markup()