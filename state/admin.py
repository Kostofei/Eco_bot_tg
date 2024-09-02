from aiogram.fsm.state import StatesGroup, State


class AddManager(StatesGroup):
    user_id = State()
