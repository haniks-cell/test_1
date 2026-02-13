from aiogram.fsm.state import StatesGroup, State

class AddGroup(StatesGroup):
    name = State()

class AddAsk(StatesGroup):
    idname = State()
    difflvl= State()
    body = State()
    
class AddCfg(StatesGroup):
    cfg = State()
    quest = State()
    is_end = State()