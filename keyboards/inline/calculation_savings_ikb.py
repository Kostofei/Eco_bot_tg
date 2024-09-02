from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .general import UserCallbackData


async def generate_inline_keyboard(callback_data: UserCallbackData = None):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=str(i),
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': "Calculation",
                        'action': callback_data.action,
                        'details': str(i)
                    }).pack()
                ) for i in range(5)
            ],
            [
                InlineKeyboardButton(
                    text=str(i),
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': "Calculation",
                        'action': callback_data.action,
                        'details': str(i)
                    }).pack()
                ) for i in range(5, 10)
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': 'main_menu',
                        'action': 'open'
                    }).pack()
                )
            ]
        ]
    )
    return keyboard


async def confirm_ikb(callback_data: UserCallbackData = None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да",
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': 'Calculation',
                        'action': 'confirm'
                    }).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': 'main_menu',
                        'action': 'open'
                    }).pack()
                )
            ]
        ]
    )
