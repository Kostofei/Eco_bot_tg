from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from config import CONFIG
from keyboards.inline.general import UserCallbackData
from keyboards.inline.calculation_savings_ikb import generate_inline_keyboard, confirm_ikb
from utils.channel import is_subscription
from utils.queue import queue
from models import User, SavingCalculation

calculation_router = Router()


@calculation_router.callback_query(UserCallbackData.filter((F.target == "Calculation") & (F.action == "main")))
async def calculation_saving(callback: CallbackQuery, callback_data: UserCallbackData, state: FSMContext):
    await callback.message.delete()

    callback_data.user_id = callback.from_user.id
    callback_data.chat_id = CONFIG.CHAT_ID

    result = await is_subscription(callback=callback, callback_data=callback_data)

    if result:
        user = await User.get(pk=callback.from_user.id)
        calculation = await SavingCalculation.all(user_id=user.id)

        if calculation:
            await callback.message.answer(
                text="У вас уже есть расчет экономии\n\n"
                     f"Мужчин - {calculation[0].men}\n"
                     f"Женщин - {calculation[0].women}\n"
                     f"Детей до 5 лет - {calculation[0].children_under_5_yo}\n\n"
                     f"Детей от 5 до 14 лет - {calculation[0].children_after_5_yo}\n\n"
                     f"Желаете произвести новый расчет?",
                reply_markup=await confirm_ikb(callback_data=callback_data)
            )
        else:
            await state.clear()

            callback_data.gift = None
            callback_data.dialog_id = None
            callback_data.chat_id = None
            callback_data.user_id = None
            callback_data.action = "man"
            callback_data.details = "man"

            await callback.message.answer(
                text='✅ Твоя  заявка на "Расчет экономии" принята\n'
                     '🎁 А также тебя ждёт приятный БОНУС\n'
                     '👉 Для того, чтобы индивидуальная экономия  была рассчитана максимально правильно, ответь, '
                     ' пожалуйста, на несколько вопросов о составе семьи\n\n'
                     'Сколько мужчин старше 14 лет',
                reply_markup=await generate_inline_keyboard(callback_data=callback_data),
                parse_mode="HTML"
            )


@calculation_router.callback_query(UserCallbackData.filter((F.target == "Calculation") & (F.action == "man")))
async def calculation_men(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: UserCallbackData,
):
    await state.update_data(man=callback_data.details)

    callback_data.action = "woman"
    callback_data.details = "woman"

    await callback.message.edit_text(
        text="Сколько женщин старше 14 лет",
        reply_markup=await generate_inline_keyboard(callback_data=callback_data),
        parse_mode="HTML"
    )


@calculation_router.callback_query(UserCallbackData.filter((F.target == "Calculation") & (F.action == "woman")))
async def calculation_women(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: UserCallbackData,
):
    await state.update_data(woman=callback_data.details)

    callback_data.action = "children_do5"
    callback_data.details = "children_do5"

    await callback.message.edit_text(
        text="Сколько детей до 5-ти лет",
        reply_markup=await generate_inline_keyboard(callback_data=callback_data),
        parse_mode="HTML"
    )


@calculation_router.callback_query(UserCallbackData.filter((F.target == "Calculation") & (F.action == "children_do5")))
async def calculation_women(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: UserCallbackData,
):
    await state.update_data(children_under_5_yo=callback_data.details)

    callback_data.action = "children_do14"
    callback_data.details = "children_do14"

    await callback.message.edit_text(
        text="Сколько детей от 5 до 14 лет",
        reply_markup=await generate_inline_keyboard(callback_data=callback_data),
        parse_mode="HTML"
    )


@calculation_router.callback_query(UserCallbackData.filter((F.target == "Calculation") & (F.action == "children_do14")))
async def calculation_children(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: UserCallbackData,
):
    data = await state.get_data()
    user = await User.get(pk=callback.from_user.id)
    calculation = await SavingCalculation.all(user_id=user.id)

    if calculation:
        await calculation[0].delete()

    calculation = SavingCalculation(
        men=str(data['man']),
        women=str(data['woman']),
        children_under_5_yo=str(data['children_under_5_yo']),
        children_after_5_yo=str(callback_data.details),
        user_id=user.id
    )
    await calculation.save()

    await state.clear()

    send_text = "Опрос на расчет экономии пройден\n\n" \
                f"мужчин - {str(data['man'])}\n"\
                f"женщин - {str(data['woman'])}\n"\
                f"Детей до 5 лет - {str(data['children_under_5_yo'])}\n\n"\
                f"Детей от 5 до 14 лет - {str(callback_data.details)}\n\n"

    callback_data.user_id = callback.from_user.id
    callback_data.details = send_text

    await queue(callback=callback, callback_data=callback_data)


@calculation_router.callback_query(UserCallbackData.filter((F.target == "Calculation") & (F.action == "confirm")))
async def calculation_confirm_men(
        callback: CallbackQuery,
        callback_data: UserCallbackData,
        state: FSMContext
):
    await state.clear()

    callback_data.gift = None
    callback_data.dialog_id = None
    callback_data.chat_id = None
    callback_data.user_id = None
    callback_data.action = "man"
    callback_data.details = "man"

    await callback.message.edit_text(
        text='✅ Твоя  заявка на "Расчет экономии" принята\n'
             '🎁 А также тебя ждёт приятный БОНУС\n'
             '👉 Для того, чтобы индивидуальная экономия  была рассчитана максимально правильно, ответь,'
             ' пожалуйста, на несколько вопросов о составе семьи\n\n'
             'Сколько мужчин старше 14 лет',
        reply_markup=await generate_inline_keyboard(callback_data=callback_data),
        parse_mode="HTML"
    )
