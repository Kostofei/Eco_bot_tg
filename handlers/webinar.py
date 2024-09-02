from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline.general import UserCallbackData
from utils.queue import queue

webinar_router = Router()


@webinar_router.callback_query(UserCallbackData.filter((F.target == "Webinar") & (F.action == "main")))
async def webinar(callback: CallbackQuery, callback_data: UserCallbackData):
    callback_data.user_id = callback.from_user.id
    await queue(callback=callback, callback_data=callback_data)
