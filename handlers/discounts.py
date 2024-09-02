from aiogram import Router, F
from aiogram.types import CallbackQuery
from models import User
from keyboards.inline.discounts import discounts_ikb
from keyboards.inline.general import UserCallbackData
from keyboards.inline.start_ikb import main_menu_ikb

discounts_router = Router()


@discounts_router.callback_query(UserCallbackData.filter((F.target == "Discounts") & (F.action == "main")))
async def discounts(callback: CallbackQuery, callback_data: UserCallbackData):
    await callback.message.delete()

    user = await User.get(pk=callback.from_user.id)

    callback_data.user_id = user.id

    if user.discounts:
        text = ('👉 Теперь ты будешь получать актуальную информацию\n\n'
                '‼️ Чтобы отписаться от рассылки АКЦИЙ/СКИДОК, перейди по кнопке <b>Назад</b> '
                'и нажми <b>Отменить подписку</b>')
    else:
        text = ("⭕️ Если ты хочешь, чтобы я сообщал тебе о всех выгодных предложениях:\n"
                "АКЦИЯХ\n"
                "СКИДКАХ\n"
                "➡️ жми на кнопку ниже 👇")

    await callback.message.answer(
        text=text,
        reply_markup=await discounts_ikb(callback_data=callback_data),
        parse_mode="HTML"
    )


@discounts_router.callback_query(UserCallbackData.filter((F.target == "Discounts") & (F.action == "subscription")))
async def subscription(callback: CallbackQuery, callback_data: UserCallbackData):
    user = await User.get(pk=callback.from_user.id)
    if user.discounts:
        await callback.message.edit_text(
            text="Вы уже подписались на рассылку",
            reply_markup=await main_menu_ikb()
            )
    else:
        user.discounts = True
        await user.save()
        await callback.message.edit_text(
            text="👉 Теперь ты будешь получать актуальную информацию\n\n",
            reply_markup=await main_menu_ikb(),
            parse_mode="HTML"
            )


@discounts_router.callback_query(UserCallbackData.filter((F.target == "Discounts") & (F.action == "unsubscription")))
async def unsubscription(callback: CallbackQuery, callback_data: UserCallbackData):
    user = await User.get(pk=callback.from_user.id)
    if user.discounts:
        user.discounts = False
        await user.save()

        await callback.message.edit_text(
            text="Подписка отменена, но ты всегда можешь ее восстановить",
            reply_markup=await main_menu_ikb()
        )
