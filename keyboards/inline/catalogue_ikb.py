from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .general import UserCallbackData


async def catalogue_ikb(callback_data: UserCallbackData = None):
    if callback_data is None:
        callback_data = UserCallbackData(
            target='main_menu',
            action='open'
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="ПОЛНЫЙ КАТАЛОГ",
                    url="https://clck.ru/3Bfxnn"
                )
            ],
            [
                InlineKeyboardButton(
                    text="КАТАЛОГ ВИТАМИНОВ И БАДОВ",
                    url="https://clck.ru/3BATh7"
                )
            ],
            [
                InlineKeyboardButton(
                    text="КАТАЛОГ ДУХОВ",
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': 'Catalogue',
                        'action': 'error'
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
