import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from models.models import User
from config import CONFIG
from keyboards.inline.gift_ikb import gift_ikb, pick_gift
from keyboards.inline.general import UserCallbackData
from utils.channel import is_subscription
from utils.queue import queue
from config.config import bot

gift_router = Router()


@gift_router.message(F.text, Command("gift"))
async def gift_command(message: Message):
    await message.delete()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except TelegramBadRequest:
        pass
    await message.answer(
        text="Выбирай себе любой подарок."
             "Список подарков постоянно пополняется ❤️",
        reply_markup=await gift_ikb()
    )


@gift_router.callback_query(UserCallbackData.filter((F.target == 'Gift') & (F.action == 'main')))
async def gift(callback: CallbackQuery, callback_data: UserCallbackData):
    await callback.message.answer(
        text="Выбирай себе любой подарок."
             "Список подарков постоянно пополняется ❤️",
        reply_markup=await gift_ikb(callback_data=callback_data)
    )


@gift_router.callback_query(UserCallbackData.filter((F.target == 'Gift') & (F.action == 'deficits')))
async def deficits(callback: CallbackQuery, callback_data: UserCallbackData):
    link_on_gift = "https://drive.google.com/file/d/12RgQY5pOoReWThFSLj7Vekdgy37Uqsxx/view"

    callback_data.user_id = callback.from_user.id
    callback_data.chat_id = CONFIG.CHAT_ID

    result = await is_subscription(callback=callback, callback_data=callback_data)

    if result:
        user = await User.get(pk=callback.from_user.id)
        if not user.first_gift_name:
            user.first_gift_name = link_on_gift
            await user.save()

        callback_data.details = link_on_gift

        await callback.message.edit_text(
            text=f"✅ Подписка проверена!!!\n\n"
                 f"💫 Поздравляю!!!\n"
                 f"Забирай 👇 подарок 🎁",
            reply_markup=await pick_gift(callback_data=callback_data)
        )

        callback_data.gift = 'Дефициты у детей'

        await queue(callback=callback, callback_data=callback_data)
        await callback.message.answer(
            text=f"Для большей эффективности направляю тебя на личного консультанта.\n"
                 f"Ты сможешь задать ему любой вопрос."
        )


@gift_router.callback_query(UserCallbackData.filter((F.target == 'Gift') & (F.action == 'swellings')))
async def swellings(callback: CallbackQuery, callback_data: UserCallbackData):
    link_on_gift = "https://drive.google.com/file/d/19hvLi4ovBAzpmTT_qcAyk-uuEfp-NttD/view"

    callback_data.user_id = callback.from_user.id
    callback_data.chat_id = CONFIG.CHAT_ID

    result = await is_subscription(callback=callback, callback_data=callback_data)

    if result:
        user = await User.get(pk=callback.from_user.id)
        if not user.first_gift_name:
            user.first_gift_name = link_on_gift
            await user.save()

        callback_data.details = link_on_gift

        await callback.message.edit_text(
            text=f"✅ Подписка проверена!!!\n\n"
                 f"💫 Поздравляю!!!\n"
                 f"Забирай 👇 подарок 🎁",
            parse_mode="HTML",
            reply_markup=await pick_gift(callback_data=callback_data)
        )

        callback_data.gift = 'Упражнения от отеков'

        await queue(callback=callback, callback_data=callback_data)
        await callback.message.answer(
            text=f"Для большей эффективности направляю тебя на личного консультанта.\n"
                 f"Ты сможешь задать ему любой вопрос."
        )


@gift_router.callback_query(UserCallbackData.filter((F.target == 'Gift') & (F.action == 'AROMAT')))
async def aromat(callback: CallbackQuery, callback_data: UserCallbackData):
    link_on_gift = "https://drive.google.com/file/d/1XLsUQh02BcRcOoeY1mXy_r6rKy1j7giq/view"

    callback_data.user_id = callback.from_user.id
    callback_data.chat_id = CONFIG.CHAT_ID

    result = await is_subscription(callback=callback, callback_data=callback_data)

    if result:
        user = await User.get(pk=callback.from_user.id)
        if not user.first_gift_name:
            user.first_gift_name = link_on_gift
            await user.save()

        callback_data.details = link_on_gift

        await callback.message.edit_text(
            text=f"✅ Подписка проверена!!!\n\n"
                 f"💫 Поздравляю!!!\n"
                 f"Забирай 👇 подарок 🎁",
            parse_mode="HTML",
            reply_markup=await pick_gift(callback_data=callback_data)
        )

        callback_data.gift = 'Подобрать свой аромат духов'

        await queue(callback=callback, callback_data=callback_data)
        await callback.message.answer(
            text=f"Для большей эффективности направляю тебя на личного консультанта.\n"
                 f"Ты сможешь задать ему любой вопрос."
        )


@gift_router.callback_query(UserCallbackData.filter((F.target == 'Gift') & (F.action == 'lifehacks')))
async def lifehacks(callback: CallbackQuery, callback_data: UserCallbackData):
    link_on_gift = "https://drive.google.com/file/d/1C59K6X870dB-4h3CHQ2kj5WXw1qqvlxj/view"

    callback_data.user_id = callback.from_user.id
    callback_data.chat_id = CONFIG.CHAT_ID

    result = await is_subscription(callback=callback, callback_data=callback_data)

    if result:
        user = await User.get(pk=callback.from_user.id)
        if not user.first_gift_name:
            user.first_gift_name = link_on_gift
            await user.save()

        callback_data.details = link_on_gift

        await callback.message.edit_text(
            text=f"✅ Подписка проверена!!!\n\n"
                 f"💫 Поздравляю!!!\n"
                 f"Забирай 👇 подарок 🎁",
            parse_mode="HTML",
            reply_markup=await pick_gift(callback_data=callback_data)
        )

        callback_data.gift = '5 лайфхаков после ремонта'

        await queue(callback=callback, callback_data=callback_data)
        await callback.message.answer(
            text=f"Для большей эффективности направляю тебя на личного консультанта.\n"
                 f"Ты сможешь задать ему любой вопрос."
        )


@gift_router.callback_query(UserCallbackData.filter((F.target == 'Gift') & (F.action == 'family')))
async def family(callback: CallbackQuery, callback_data: UserCallbackData):
    link_on_gift = "https://drive.google.com/file/d/1gSQmKFyLEsEmFJY8s5e_3IpZzTjQaiTv/view"

    callback_data.user_id = callback.from_user.id
    callback_data.chat_id = CONFIG.CHAT_ID

    result = await is_subscription(callback=callback, callback_data=callback_data)

    if result:
        user = await User.get(pk=callback.from_user.id)
        if not user.first_gift_name:
            user.first_gift_name = link_on_gift
            await user.save()

        callback_data.details = link_on_gift

        await callback.message.edit_text(
            text=f"✅ Подписка проверена!!!\n\n"
                 f"💫 Поздравляю!!!\n"
                 f"Забирай 👇 подарок 🎁",
            parse_mode="HTML",
            reply_markup=await pick_gift(callback_data=callback_data)
        )

        callback_data.gift = 'Уловки семейного бюджета'

        await queue(callback=callback, callback_data=callback_data)
        await callback.message.answer(
            text=f"Для большей эффективности направляю тебя на личного консультанта.\n"
                 f"Ты сможешь задать ему любой вопрос."
        )


@gift_router.callback_query(UserCallbackData.filter((F.target == 'Gift') & (F.action == 'TOP5')))
async def top5(callback: CallbackQuery, callback_data: UserCallbackData):
    link_on_gift = "https://drive.google.com/file/d/1uibD0bjSHakVH6nuT6g0K5_ReqQW36MP/view"

    callback_data.user_id = callback.from_user.id
    callback_data.chat_id = CONFIG.CHAT_ID

    result = await is_subscription(callback=callback, callback_data=callback_data)

    if result:
        user = await User.get(pk=callback.from_user.id)
        if not user.first_gift_name:
            user.first_gift_name = link_on_gift
            await user.save()

        callback_data.details = link_on_gift

        await callback.message.edit_text(
            text=f"✅ Подписка проверена!!!\n\n"
                 f"💫 Поздравляю!!!\n"
                 f"Забирай 👇 подарок 🎁",
            parse_mode="HTML",
            reply_markup=await pick_gift(callback_data=callback_data)
        )

        callback_data.gift = 'ТОП-5 вредных веществ в креме'

        await queue(callback=callback, callback_data=callback_data)
        await callback.message.answer(
            text=f"Для большей эффективности направляю тебя на личного консультанта.\n"
                 f"Ты сможешь задать ему любой вопрос."
        )


@gift_router.callback_query(UserCallbackData.filter((F.target == 'Gift') & (F.action == 'relaxations')))
async def relaxations(callback: CallbackQuery, callback_data: UserCallbackData):
    link_on_gift = "https://drive.google.com/file/d/1lqc5HpcWyN34JAICzTOBGT7zCgowTZAk/view"

    callback_data.user_id = callback.from_user.id
    callback_data.chat_id = CONFIG.CHAT_ID

    result = await is_subscription(callback=callback, callback_data=callback_data)

    if result:
        user = await User.get(pk=callback.from_user.id)
        if not user.first_gift_name:
            user.first_gift_name = link_on_gift
            await user.save()

        callback_data.details = link_on_gift

        await callback.message.edit_text(
            text=f"✅ Подписка проверена!!!\n\n"
                 f"💫 Поздравляю!!!\n"
                 f"Забирай 👇 подарок 🎁",
            parse_mode="HTML",
            reply_markup=await pick_gift(callback_data=callback_data)
        )

        callback_data.gift = 'Техники расслабления'

        await queue(callback=callback, callback_data=callback_data)
        await callback.message.answer(
            text=f"Для большей эффективности направляю тебя на личного консультанта.\n"
                 f"Ты сможешь задать ему любой вопрос."
        )


@gift_router.callback_query(UserCallbackData.filter((F.target == 'Gift') & (F.action == 'Makeup')))
async def make_up(callback: CallbackQuery, callback_data: UserCallbackData):
    link_on_gift = "https://drive.google.com/file/d/1Ck2l5DVbT-BiI9i6I1ePY0JaYFXBqAWz/view"

    callback_data.user_id = callback.from_user.id
    callback_data.chat_id = CONFIG.CHAT_ID

    result = await is_subscription(callback=callback, callback_data=callback_data)

    if result:
        user = await User.get(pk=callback.from_user.id)
        if not user.first_gift_name:
            user.first_gift_name = link_on_gift
            await user.save()

        callback_data.details = link_on_gift

        await callback.message.edit_text(
            text=f"✅ Подписка проверена!!!\n\n"
                 f"💫 Поздравляю!!!\n"
                 f"Забирай 👇 подарок 🎁",
            parse_mode="HTML",
            reply_markup=await pick_gift(callback_data=callback_data)
        )

        callback_data.gift = 'Макияж за 10 минут'

        await queue(callback=callback, callback_data=callback_data)
        await callback.message.answer(
            text=f"Для большей эффективности направляю тебя на личного консультанта.\n"
                 f"Ты сможешь задать ему любой вопрос."
        )
