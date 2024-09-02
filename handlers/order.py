from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline.general import UserCallbackData
from utils.queue import queue

order_router = Router()


@order_router.callback_query(UserCallbackData.filter((F.target == "Order") & (F.action == "main")))
async def order(callback: CallbackQuery, callback_data: UserCallbackData):
    send_text = 'нужна консультация по продукту. Прошел по кнопке "Заказать"'

    callback_data.user_id = callback.from_user.id
    callback_data.details = send_text

    await queue(callback=callback, callback_data=callback_data)
