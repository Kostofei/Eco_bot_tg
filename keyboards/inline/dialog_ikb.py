from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .general import DialogCallbackData


async def answer_for_manager_ikb(callback_data: DialogCallbackData) -> InlineKeyboardMarkup:
    if callback_data.details == "question":
        buttons = [
            [
                InlineKeyboardButton(
                    text="Задать вопрос",
                    callback_data=DialogCallbackData(**callback_data.model_dump() | {
                        'target': 'Dialog',
                        'action': 'answer_for_manager',
                        'dialog_id': callback_data.dialog_id
                    }).pack()
                )
            ]
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    text="Ответить",
                    callback_data=DialogCallbackData(**callback_data.model_dump() | {
                        'target': 'Dialog',
                        'action': 'answer_for_manager',
                        'dialog_id': callback_data.dialog_id
                    }).pack()
                )
            ]
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def answer_for_user_dialog_ikb(callback_data: DialogCallbackData) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Ответить",
                callback_data=DialogCallbackData(**callback_data.model_dump() | {
                    'target': 'Dialog',
                    'action': 'answer_for_user',
                    'dialog_id': callback_data.dialog_id
                }).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
