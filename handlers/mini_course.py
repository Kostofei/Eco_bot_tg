from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline.general import UserCallbackData
from keyboards.inline.start_ikb import main_menu_ikb
from utils.mini_cuorce import Course
from models import User, MiniCourse
from utils.channel import is_subscription
from config import CONFIG
from datetime import datetime


mini_course_router = Router()


@mini_course_router.callback_query(UserCallbackData.filter((F.target == "Mini_course") & (F.action == "main")))
async def mini_course(callback: CallbackQuery, callback_data: UserCallbackData):
    await callback.message.delete()

    user = await User.get(pk=callback.from_user.id)
    get_course = await MiniCourse.all(user_id=user.id)

    callback_data.user_id = callback.from_user.id
    callback_data.chat_id = CONFIG.CHAT_ID

    result = await is_subscription(callback=callback, callback_data=callback_data)

    if result:
        if not get_course:
            if datetime.now().time().hour >= 19:
                new_mini_course = MiniCourse(
                    user_id=user.id,
                    day_one=True
                )
                await new_mini_course.save()
            else:
                new_mini_course = MiniCourse(
                    user_id=user.id,
                    day_two=True
                )
            await new_mini_course.save()

            await Course.start(callback=callback, callback_data=callback_data)

        else:
            await callback.message.answer(
                text=f"Вы уже записались на курс!\n"
                     f"Утром и вечером будут приходить уведомления.",
                reply_markup=await main_menu_ikb(callback_data=callback_data)
            )
