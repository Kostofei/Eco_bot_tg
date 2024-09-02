from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.general import UserCallbackData
from models import User


async def discounts_ikb(callback_data: UserCallbackData = None) -> InlineKeyboardMarkup:
    user = await User.get(pk=callback_data.user_id)

    if user.discounts:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Отменить подписку",
                        callback_data=UserCallbackData(**callback_data.model_dump() | {
                            'target': 'Discounts',
                            'action': 'unsubscription'
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
    else:

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Подписаться",
                        callback_data=UserCallbackData(**callback_data.model_dump() | {
                            'target': 'Discounts',
                            'action': 'subscription'
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
