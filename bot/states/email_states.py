from aiogram.fsm.state import StatesGroup, State

class EmailStates(StatesGroup):
    send_email = State()