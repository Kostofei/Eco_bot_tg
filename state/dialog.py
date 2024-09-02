from aiogram.fsm.state import StatesGroup, State


class DialogForUserState(StatesGroup):
    dialog_id = State()
    sms = State()
    details = State()


class DialogForManagerState(StatesGroup):
    dialog_id = State()
    sms = State()
    details = State()
