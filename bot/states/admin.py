from aiogram.fsm.state import StatesGroup, State

class AdminBroadcast(StatesGroup):
    waiting_text = State()
    waiting_segment = State()
    waiting_confirm = State()
