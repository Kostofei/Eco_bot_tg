from datetime import datetime
from aiogram import F, Router, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.deep_linking import decode_payload
from config.config import bot
from models import User, Dialog
from keyboards.inline.general import UserCallbackData
from keyboards.inline import start_ikb

start_router = Router()


@start_router.message(CommandStart(deep_link=True))
async def start_with_link(message: Message, command: CommandObject):
    user = await User.get(pk=message.from_user.id)
    args = command.args
    payload = decode_payload(args)

    if not user:
        user = User(id=message.from_user.id,
                    tg_first_name=message.from_user.first_name,
                    tg_last_name=message.from_user.last_name,
                    tg_username=message.from_user.username
                    )
        await user.save()

        await bot.send_message(
            chat_id=int(payload),
            text=f"По вашей ссылке зарегистрировался человек:"
                 f" {message.from_user.first_name} {message.from_user.last_name}"
        )

        dialog = Dialog(
            user_id=user.id,
            created_at=datetime.now(),
            is_active=True,
            manager_id=int(payload)
            )
        await dialog.save()

        # photo = types.FSInputFile("media/start.jpg")
        photo = types.FSInputFile("/opt/git/EchoBot/media/start.jpg")

        await message.answer_photo(
            photo=photo,
            caption="🌏 Приветствую в ЭКОботе 🌏\n"
                    "Если Главное меню бота будет скрыто, то нажми синюю кнопку Меню внизу экрана\n"
                    "👇 А сейчас выбери интересующий раздел",
            reply_markup=await start_ikb()
        )


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.delete()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except TelegramBadRequest:
        pass

    await state.clear()

    # photo = types.FSInputFile("media/start.jpg")
    photo = types.FSInputFile("/opt/git/EchoBot/media/start.jpg")

    if await User.get(pk=message.from_user.id):

        await message.answer_photo(
            photo=photo,
            caption="🌏 Приветствую в ЭКОботе 🌏\n"
                    "Если Главное меню бота будет скрыто, то нажми синюю кнопку Меню внизу экрана\n"
                    "👇 А сейчас выбери интересующий раздел",
            reply_markup=await start_ikb()
        )

    else:
        user = User(
            id=message.from_user.id,
            tg_first_name=message.from_user.first_name,
            tg_last_name=message.from_user.last_name,
            tg_username=message.from_user.username
            )
        await user.save()
        await message.answer_photo(
            photo=photo,
            caption="🌏 Приветствую в ЭКОботе 🌏\n"
                    "Если Главное меню бота будет скрыто, то нажми синюю кнопку Меню внизу экрана\n"
                    "👇 А сейчас выбери интересующий раздел",
            reply_markup=await start_ikb()
        )


@start_router.callback_query(UserCallbackData.filter((F.target == 'main_menu') & (F.action == 'open')))
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()

    # photo = types.FSInputFile("media/start.jpg")
    photo = types.FSInputFile("/opt/git/EchoBot/media/start.jpg")

    if await User.get(pk=callback.from_user.id):
        await callback.message.answer_photo(
            photo=photo,
            caption="🌏 Приветствую в ЭКОботе 🌏\n"
                    "Если Главное меню бота будет скрыто, то нажми синюю кнопку Меню внизу экрана\n"
                    "👇 А сейчас выбери интересующий раздел",
            reply_markup=await start_ikb()
        )
