from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from keyboards.inline.catalogue_ikb import catalogue_ikb
from keyboards.inline.general import UserCallbackData
from config.config import bot

catalogue_router = Router()


@catalogue_router.message(F.text, Command("catalogue"))
async def catalogue_command(message: Message):
    await message.delete()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except TelegramBadRequest:
        pass
    try:
        await message.answer_photo(
            photo="https://play-lh.googleusercontent.com/UButs8zTPt-7HO-"
                  "Y7gv5OoHScRDTplFGSrlxSSj8BnztAjxSjnWnhQqt51I114REJnnF",
            caption="Выбирай интересующий раздел 👇",
            reply_markup=await catalogue_ikb()
        )
    except TelegramBadRequest:
        await message.answer(
            text="Выбирай интересующий раздел 👇",
            reply_markup=await catalogue_ikb()
        )


@catalogue_router.callback_query(UserCallbackData.filter((F.target == "Catalogue") & (F.action == "main")))
async def catalogue(callback: CallbackQuery, callback_data: UserCallbackData):
    await callback.message.delete()

    try:
        await callback.message.answer_photo(
            photo="https://play-lh.googleusercontent.com/UButs8zTPt-7HO-"
                  "Y7gv5OoHScRDTplFGSrlxSSj8BnztAjxSjnWnhQqt51I114REJnnF",
            caption="Выбирай интересующий раздел 👇",
            reply_markup=await catalogue_ikb(callback_data=callback_data)
        )
    except TelegramBadRequest:
        await callback.message.answer(
            text="Выбирай интересующий раздел 👇",
            reply_markup=await catalogue_ikb(callback_data=callback_data)
        )


@catalogue_router.callback_query(UserCallbackData.filter((F.target == "Catalogue") & (F.action == "error")))
async def catalogue_error(callback: CallbackQuery):
    await callback.message.answer(
        text=f'Приносим свои извинения.\n'
             f'Электронный каталог находится на доработке.\n\n'
             f'Если вы хотите узнать подробно о каком-либо продукте, то напишите свой вопрос в строке Сообщение'
    )
