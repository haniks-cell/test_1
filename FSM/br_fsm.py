from aiogram.fsm.state import StatesGroup, State

class AddGroup(StatesGroup):
    name = State()

class AddAsk(StatesGroup):
    idname = State()
    difflvl= State()
    body = State()
    