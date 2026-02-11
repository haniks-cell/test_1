import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keybords.br import startbr, diffkb
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from FSM.br_fsm import AddGroup, AddAsk

from database.models import Group, Question
from keybords.keyboards import repkeyb, inlkeyb, create_inline, startkb, create_reply

router = Router()

@router.callback_query(F.data == 'br_start')
async def ress (callback: types.CallbackQuery, session: AsyncSession):
    # session.add(Question(idname=1, body='one' ))
    # await session.commit()
    await callback.answer('')
    await callback.message.edit_text('Выберите действие', reply_markup=startbr)

@router.callback_query(StateFilter(None), F.data == 'br_addgrop')
async def add_group (callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddGroup.name)
    await callback.message.answer('Введите назване группы')
    # await callback.message.edit_text('Выберите действие', reply_markup=startbr)

@router.message(AddGroup.name)
async def inpName (message: types.Message, session: AsyncSession, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await state.clear()
    session.add(Group(name=data['name']))
    await session.commit()
    await message.answer(f'Группа {data['name']} успешно добавлена')
    await message.answer('Выберите действие', reply_markup=startbr)

@router.callback_query(StateFilter(None), F.data == 'br_addask')
async def add_group (callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    # await state.set_state(AddAsk.idname)
    query = select(Group)
    res = await session.execute(query)
    result = res.unique().scalars().all()
    await state.set_state(AddAsk.idname)
    await callback.message.answer('Выбирете группу', reply_markup=await create_reply(result))

@router.message(AddAsk.idname)
async def inpIdname (message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddAsk.difflvl)
    await message.answer('Введите уровень сложности вопроса', reply_markup=diffkb)
    # await message.answer('Введите сам вопрос с заглавной буквы', reply_markup=ReplyKeyboardRemove())

@router.message(AddAsk.difflvl)
async def inpIdname (message: types.Message, state: FSMContext):
    await state.update_data(difflvl=message.text)
    await state.set_state(AddAsk.body)
    # await message.answer('Введите уровень сложности вопроса', reply_markup=diffkb)
    await message.answer('Введите сам вопрос с заглавной буквы', reply_markup=ReplyKeyboardRemove())


@router.message(AddAsk.body)
async def inpIdname (message: types.Message, session: AsyncSession, state: FSMContext):
    await state.update_data(body=message.text)
    data = await state.get_data()
    await state.clear()

    query = select(Group).where(Group.name == data["name"])
    res = await session.execute(query)
    result = res.scalar()
    # await message.answer(str(result.tid))

    session.add(Question(idname=result.tid, difflvl=int(data["difflvl"]), body=data["body"]))
    await session.commit()

    await message.answer('Вопрос успешно добавлен')

@router.callback_query(StateFilter(None), F.data == 'br_addcfg')
async def ress (callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    # session.add(Question(idname=1, body='one' ))
    # await session.commit()
    # await callback.answer('')
    # await callback.message.edit_text('Выберите действие', reply_markup=startbr)
    query = select(Group)
    res = await session.execute(query)
    result = res.unique().scalars().all()

    await state.set_state(AddAsk.idname)
    await callback.message.answer('Выбирете группу', reply_markup=await create_reply(result))
