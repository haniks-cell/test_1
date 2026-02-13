from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

startbr = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить шаблон', callback_data='br_getshb')],
    [InlineKeyboardButton(text='Добавить Конфигурацию', callback_data='br_addcfg')],
    [InlineKeyboardButton(text='Добавить вопрос', callback_data='br_addask')],
    [InlineKeyboardButton(text='Добавить группу', callback_data='br_addgrop')]
], resize_keyboard=True)

diffkb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='1'), KeyboardButton(text='2'), KeyboardButton(text='3')],
    [KeyboardButton(text='4'),KeyboardButton(text='5')]
], resize_keyboard=True)

is_endkb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Конец'), KeyboardButton(text='Продолжить')]
], resize_keyboard=True)