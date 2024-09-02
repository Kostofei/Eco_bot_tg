from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.general import UserCallbackData, ManagerCallbackData
from models.models import Dialog, User


async def manager_menu_ikb(callback_data: ManagerCallbackData = None) -> InlineKeyboardMarkup:
    if callback_data is None:
        callback_data = ManagerCallbackData(
            target='manager_menu',
            action='open'
        )

    buttons = [
        [
            InlineKeyboardButton(
                text="Мои диалоги",
                callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                    'target': 'Manager',
                    'action': 'show_all_my_dialogs'
                }).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Моя ссылка",
                callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                    'target': 'Manager',
                    'action': 'show_my_link'
                }).pack()
            )
        ]
    ]

    back = [
        InlineKeyboardButton(
            text="Выход",
            callback_data=UserCallbackData(**callback_data.model_dump() | {
                'target': 'main_menu',
                'action': 'open'
            }).pack()
        )
    ]
    buttons.append(back)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def show_all_my_dialogs_ikb(callback_data: ManagerCallbackData = None):
    dialogs = await Dialog.all(manager_id=callback_data.manager_id)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{(await User.get(pk=dialog.user_id)).tg_first_name} "
                     f"{(await User.get(pk=dialog.user_id)).tg_last_name}",
                callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                    'target': 'Manager',
                    'action': 'get_dialog',
                    'dialog_id': dialog.id
                }).pack()
            )
        ] for dialog in dialogs
    ]

    search = [
        InlineKeyboardButton(
            text="Поиск диалога",
            callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                'target': 'Manager',
                'action': 'search_dialog'
            }).pack()
        )
    ]
    end = [
        InlineKeyboardButton(
            text="Назад",
            callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                'target': 'manager_menu',
                'action': 'open'
            }).pack()
        )
    ]
    buttons.append(search)
    buttons.append(end)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def dialog_with_user_ikb(callback_data: ManagerCallbackData = None) -> InlineKeyboardMarkup:
    if callback_data is None:
        callback_data = ManagerCallbackData(
            target='manager_menu',
            action='open'
        )
    buttons = [
        [
            InlineKeyboardButton(
                text="Написать",
                callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                    'target': 'Dialog',
                    'action': 'get_sms_for_user',
                    'details': 'mng_menu'
                }).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Отправить подарок",
                callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                    'target': 'Manager',
                    'action': 'send_gift'
                }).pack()
            )
        ],
    ]

    end = [
        InlineKeyboardButton(
            text="Назад",
            callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                'target': 'Manager',
                'action': 'show_all_my_dialogs'
            }).pack()
        )
    ]
    buttons.append(end)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def back_dialog_with_user_ikb(callback_data: ManagerCallbackData = None) -> InlineKeyboardMarkup:
    if callback_data is None:
        callback_data = ManagerCallbackData(
            target='manager_menu',
            action='open'
        )
    buttons = [
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                    'target': 'Manager',
                    'action': 'get_dialog'
                }).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def back_all_dialogs_ikb(callback_data: ManagerCallbackData = None) -> InlineKeyboardMarkup:
    if callback_data is None:
        callback_data = ManagerCallbackData(
            target='manager_menu',
            action='open'
        )
    buttons = [
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                    'target': 'Manager',
                    'action': 'show_all_my_dialogs'
                }).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def back_manager_menu_ikb(callback_data: ManagerCallbackData = None) -> InlineKeyboardMarkup:
    if callback_data is None:
        callback_data = ManagerCallbackData(
            target='manager_menu',
            action='open'
        )
    buttons = [
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                    'target': 'manager_menu',
                    'action': 'open'
                }).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def approve_search_dialog_ikb(callback_data: ManagerCallbackData = None):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да",
                    callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                        'target': 'Manager',
                        'action': 'search_again'
                    }).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Нет",
                    callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                        'target': 'Manager',
                        'action': 'show_all_my_dialogs'
                    }).pack()
                )
            ]
        ]
    )


async def notification_new_manager_ikb(callback_data: UserCallbackData = None) -> InlineKeyboardMarkup:
    if callback_data is None:
        callback_data = UserCallbackData(
            target='main_menu',
            action='open'
        )
    buttons = [
        [
            InlineKeyboardButton(
                text="Отлично",
                callback_data=UserCallbackData(**callback_data.model_dump() | {
                    'target': 'main_menu',
                    'action': 'open'
                }).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
