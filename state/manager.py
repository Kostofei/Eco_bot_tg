from aiogram.fsm.state import StatesGroup, State


class SearchDialog(StatesGroup):
    user_id = State()
