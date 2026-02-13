import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from FSM.br_fsm import AddGroup, AddAsk, AddCfg

from database.models import Group, Question, Configuration
from keybords.keyboards import repkeyb, inlkeyb, create_inline, startkb, create_reply
from keybords.br import startbr, diffkb, is_endkb

# from logic.br 

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
async def add_ask (callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
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
async def inpdiff (message: types.Message, state: FSMContext):
    await state.update_data(difflvl=message.text)
    await state.set_state(AddAsk.body)
    # await message.answer('Введите уровень сложности вопроса', reply_markup=diffkb)
    await message.answer('Введите сам вопрос с заглавной буквы', reply_markup=ReplyKeyboardRemove())


@router.message(AddAsk.body)
async def inpBody (message: types.Message, session: AsyncSession, state: FSMContext):
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
    await message.answer('Выберите действие', reply_markup=startbr)

@router.callback_query(StateFilter(None), F.data == 'br_addcfg')
async def addcfg (callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    query = select(Group)
    res = await session.execute(query)
    result = res.unique().scalars().all()
    await state.update_data(res=result)
    await state.set_state(AddCfg.cfg)
    await callback.message.answer('Выбирете группу', reply_markup=await create_reply(result))

@router.message(AddCfg.cfg)
async def cfg (message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    # Сразу обновляем: (старый_список или []) + [новый_элемент]
    await state.update_data(
        # quest=data.get("quest", []),
        cfg=data.get("cfg", []) + [message.text]
    )
    await state.set_state(AddCfg.quest)
    # data = await state.get_data()
    # await state.clear()
    # query = select(Group).where(Group.name == data["cfg1"])
    # res = await session.execute(query)
    # result = res.scalar()
    # cf = Configuration()
    # cf.grp.append(result)
    # session.add(cf)
    # await session.commit()
    # # await message.answer('Введите уровень сложности вопроса', reply_markup=diffkb)
    await message.answer('Введите сложность вопрос подряд, без запятых', reply_markup=ReplyKeyboardRemove())

@router.message(AddCfg.quest)
async def quest_cfg (message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    # Сразу обновляем: (старый_список или []) + [новый_элемент]
    await state.update_data(
        quest=data.get("quest", []) + [message.text]
        # cfg=data.get("cfg", [])
    )
    await state.set_state(AddCfg.is_end)
    await message.answer('Выберите продолжение', reply_markup=is_endkb)

@router.message(AddCfg.is_end)
async def quest_cfg (message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    data["res"][:] = [g for g in data["res"] if g.name != data["cfg"][-1]]
    await state.update_data(res=data["res"])
    if message.text == 'Конец':
        await state.clear()
        arrout = [list(item) for item in zip(data["cfg"], data["quest"])]
        # print(arrout)
        query = select(Group).where(Group.name.in_(data["cfg"]))
        res = await session.execute(query)
        result = res.unique().scalars().all()

        cf = Configuration(cntquest=arrout)
        cf.grp.append(result)
        session.add(cf)
        await session.commit()

        await message.answer('Конфигурация записана', reply_markup=is_endkb)
        await message.answer('Выберите действие', reply_markup=startbr)
    elif message.text == 'Продолжить':
        await state.set_state(AddCfg.cfg)
        await message.answer('Выбирете группу', reply_markup=await create_reply(data["res"]))