from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.general import UserCallbackData


async def gift_ikb(callback_data: UserCallbackData = None) -> InlineKeyboardMarkup:
    if callback_data is None:
        callback_data = UserCallbackData(
            target='main_menu',
            action='open'
        )

    data_ikb = {
        f"Мини курс: эмоциональное выгорание": {"target": "Mini_course", "action": "main", },
        f"Дефициты у детей": {"target": "Gift", "action": "deficits", },
        f"Упражнения от отеков": {"target": "Gift", "action": "swellings", },
        f"Техники расслабления": {"target": "Gift", "action": "relaxations", },
        f"Подобрать свой аромат духов": {"target": "Gift", "action": "AROMAT", },
        f"ТОП-5 вредных веществ в креме": {"target": "Gift", "action": "TOP5", },
        f"Макияж за 10 минут": {"target": "Gift", "action": "Makeup", },
        f"5 лайфхаков после ремонта": {"target": "Gift", "action": "lifehacks", },
        f"Уловки семейного бюджета": {"target": "Gift", "action": "family", },
    }

    buttons = [
        [
            InlineKeyboardButton(
                text=name,
                callback_data=UserCallbackData(**callback_data.model_dump() | {
                    'target': item['target'],
                    'action': item['action']
                }).pack()
            )
        ] for name, item in data_ikb.items()
    ]
    back = [
        InlineKeyboardButton(
            text='Назад',
            callback_data=UserCallbackData(**callback_data.model_dump() | {
                'target': 'main_menu',
                'action': 'open'
            }).pack()
        )
    ]
    buttons.append(back)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def check_subscribe_ikb(callback_data: UserCallbackData = None) -> InlineKeyboardMarkup:
    link = callback_data.details
    buttons = [
        [
            InlineKeyboardButton(
                text="Подписаться",
                url=link
            )
        ]
    ]
    callback_data.details = None
    menu = [
        InlineKeyboardButton(
            text="Готово",
            callback_data=UserCallbackData(**callback_data.model_dump() | {
                'target': callback_data.target,
                'action': callback_data.action
            }).pack()
        )
    ]
    buttons.append(menu)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def pick_gift(callback_data: UserCallbackData = None) -> InlineKeyboardMarkup:
    link = callback_data.details
    buttons = [
        [
            InlineKeyboardButton(
                text="Забрать подарок",
                url=link
            )
        ]
    ]
    callback_data.details = None
    menu = [
        InlineKeyboardButton(
            text="Главное меню",
            callback_data=UserCallbackData(**callback_data.model_dump() | {
                'target': 'main_menu',
                'action': 'open'
            }).pack()
        )
    ]
    buttons.append(menu)
    return InlineKeyboardMarkup(inline_keyboard=buttons)
