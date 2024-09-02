from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.general import UserCallbackData, AdminCallbackData, ManagerCallbackData
from models.models import User, Dialog
from emuns import UserRole


async def answer_for_user_ikb(callback_data: UserCallbackData) -> InlineKeyboardMarkup:
    dialog = await Dialog.get(pk=callback_data.dialog_id)

    buttons = []

    if callback_data.target == "Gift":
        if dialog.manager_id:
            buttons = [
                [
                    InlineKeyboardButton(
                        text="Хорошо",
                        callback_data=UserCallbackData(**callback_data.model_dump() | {
                            'target': 'Question',
                            'action': 'gift_user_second',
                            'user_id': callback_data.user_id,
                            'dialog_id': callback_data.dialog_id
                        }).pack()
                    )
                ]
            ]
        else:
            buttons = [
                [
                    InlineKeyboardButton(
                        text="Взять в работу ",
                        callback_data=UserCallbackData(**callback_data.model_dump() | {
                            'target': 'Question',
                            'action': 'gift_user',
                            'user_id': callback_data.user_id,
                            'dialog_id': callback_data.dialog_id
                        }).pack()
                    )
                ]
            ]

    if callback_data.target == "Mini_course":
        buttons = [
            [
                InlineKeyboardButton(
                    text="Отправить опрос 1",
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': 'Question',
                        'action': 'survey_user',
                        'user_id': callback_data.user_id,
                        'dialog_id': callback_data.dialog_id
                    }).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отправить опрос 2",
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': 'Question',
                        'action': 'survey_user',
                        'user_id': callback_data.user_id,
                        'dialog_id': callback_data.dialog_id
                    }).pack()
                )
            ]
        ]

    if callback_data.target == "Calculation":
        buttons = [
            [
                InlineKeyboardButton(
                    text="Выслать расчет и бонус",
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': 'Question',
                        'action': 'take_user',
                        'user_id': callback_data.user_id,
                        'dialog_id': callback_data.dialog_id
                    }).pack()
                )
            ]
        ]

    if callback_data.target == "Question":
        buttons = [
            [
                InlineKeyboardButton(
                    text="Взять в работу",
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': 'Question',
                        'action': 'take_user',
                        'user_id': callback_data.user_id,
                        'dialog_id': callback_data.dialog_id
                    }).pack()
                )
            ]
        ]

    if callback_data.target == "Order":
        buttons = [
            [
                InlineKeyboardButton(
                    text="Помочь с заказом",
                    callback_data=UserCallbackData(**callback_data.model_dump() | {
                        'target': 'Question',
                        'action': 'take_user',
                        'user_id': callback_data.user_id,
                        'dialog_id': callback_data.dialog_id
                    }).pack()
                )
            ]
        ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def admin_menu_ikb(callback_data: AdminCallbackData = None) -> InlineKeyboardMarkup:
    if callback_data is None:
        callback_data = AdminCallbackData(
            target='admin_menu',
            action='open'
        )

    buttons = [
        [
            InlineKeyboardButton(
                text="Менеджеры",
                callback_data=AdminCallbackData(**callback_data.model_dump() | {
                    'target': 'Admin',
                    'action': 'show_all_managers'
                }).pack()
            )
        ]
    ]

    go_manager_panel = [
        InlineKeyboardButton(
            text="Перейти в меню менеджера",
            callback_data=ManagerCallbackData(**callback_data.model_dump() | {
                'target': 'manager_menu',
                'action': 'open'
            }).pack()
        )
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
    buttons.append(go_manager_panel)
    buttons.append(back)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def show_all_managers_ikb(callback_data: AdminCallbackData = None):
    managers = await User.all(role=UserRole.ADMIN)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{manager.tg_first_name} id: {manager.id}",
                callback_data=AdminCallbackData(**callback_data.model_dump() | {
                    'target': 'Admin',
                    'action': 'get_manager',
                    'manager_id': manager.id
                }).pack()
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=AdminCallbackData(**callback_data.model_dump() | {
                    'target': 'Admin',
                    'action': 'del_manager',
                    'manager_id': manager.id
                }).pack()
            )
        ] for manager in managers
    ]

    end = [
        InlineKeyboardButton(
            text="➕",
            callback_data=AdminCallbackData(**callback_data.model_dump() | {
                'target': 'Admin',
                'action': 'add_manager'
            }).pack()
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=AdminCallbackData(**callback_data.model_dump() | {
                'target': 'admin_menu',
                'action': 'open'
            }).pack()
        )
    ]
    buttons.append(end)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def confirm_add_manager_ikb(callback_data: AdminCallbackData = None):
    if callback_data is None:
        callback_data = AdminCallbackData(
            target='Admin',
            action='add'
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да",
                    callback_data=AdminCallbackData(**callback_data.model_dump() | {
                        'target': 'Admin',
                        'action': 'confirm_add',
                        'details': 'yes'
                    }).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Нет",
                    callback_data=AdminCallbackData(**callback_data.model_dump() | {
                        'target': 'Admin',
                        'action': 'confirm_add',
                        'details': 'no'
                    }).pack()
                )
            ]
        ]
    )


async def confirm_del_manager_ikb(callback_data: AdminCallbackData = None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да",
                    callback_data=AdminCallbackData(**callback_data.model_dump() | {
                        'target': 'Admin',
                        'action': 'confirm_del'
                    }).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Нет",
                    callback_data=AdminCallbackData(**callback_data.model_dump() | {
                        'target': 'Admin',
                        'action': 'show_all_managers'
                    }).pack()
                )
            ]
        ]
    )


async def back_show_all_managers_ikb(callback_data: AdminCallbackData = None):
    if callback_data is None:
        callback_data = AdminCallbackData(
            target='admin_menu',
            action='open'
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=AdminCallbackData(**callback_data.model_dump() | {
                        'target': 'Admin',
                        'action': 'show_all_managers'
                    }).pack()
                )
            ]
        ]
    )
