from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .general import UserCallbackData


async def start_ikb(callback_data: UserCallbackData = None) -> InlineKeyboardMarkup:
    if callback_data is None:
        callback_data = UserCallbackData(
            target='start_menu',
            action='open'
        )

    data_ikb = {
        f"Получить подарок": {"target": "Gift", "action": "main", },
        f"Мини-курс: эмоциональное выгорание": {"target": "Mini_course", "action": "main", },
        f"Расчет экономии": {"target": "Calculation", "action": "main", },
        f"Запись на вебинар": {"target": "Webinar", "action": "main", },
        f"Задать вопрос": {"target": "Question", "action": "main", },
        f"Заказать": {"target": "Order", "action": "main", },
        f"Каталог": {"target": "Catalogue", "action": "main", },
        f"Скидки/Акции": {"target": "Discounts", "action": "main", },
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
    about = [
        InlineKeyboardButton(
            text="О нас",
            url="http://ecolife.b24site.online/"
        )
    ]
    buttons.append(about)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def main_menu_ikb(callback_data: UserCallbackData = None) -> InlineKeyboardMarkup:
    if callback_data is None:
        callback_data = UserCallbackData(
            target='main_menu',
            action='open'
        )
    buttons = [
        [
            InlineKeyboardButton(
                text="Главное меню",
                callback_data=UserCallbackData(**callback_data.model_dump() | {
                    'target': 'main_menu',
                    'action': 'open'
                }).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
