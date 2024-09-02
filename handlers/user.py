from aiogram import Router
from aiogram.types import Message, ContentType
from config.config import bot
from models import User, Dialog
from keyboards.inline.general import DialogCallbackData
from keyboards.inline.dialog_ikb import answer_for_user_dialog_ikb

user_router = Router()


@user_router.message()
async def all_sms_user(message: Message):
    user = await User.get(pk=message.from_user.id)
    dialog = await Dialog.all(user_id=user.id)

    if dialog:

        callback_data = DialogCallbackData(
            dialog_id=dialog[0].id
        )

        if message.content_type == ContentType.TEXT:
            await bot.send_message(
                chat_id=dialog[0].manager_id,
                text=f"Пользователь {user.tg_first_name} {user.tg_last_name} написал в чат с ботом:\n\n"
                     f"{message.text}",
                reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
            )

        if message.content_type == ContentType.PHOTO:
            await bot.send_photo(
                chat_id=dialog[0].manager_id,
                photo=message.photo[0].file_id,
                caption=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                        f"отправил вам это изображение",
                reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
            )

        if message.content_type == ContentType.DOCUMENT:
            await bot.send_document(
                chat_id=dialog[0].manager_id,
                document=message.document.file_id,
                caption=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                        f"отправил вам этот документ",
                reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
            )

        if message.content_type == ContentType.VIDEO:
            await bot.send_video(
                chat_id=dialog[0].manager_id,
                video=message.video.file_id,
                caption=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                        f"отправил вам это видео",
                reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
            )

        if message.content_type == ContentType.VOICE:
            await bot.send_voice(
                chat_id=dialog[0].manager_id,
                voice=message.voice.file_id,
                caption=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                        f"отправил вам это голосовое сообщение",
                reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
            )

        if message.content_type == ContentType.VIDEO_NOTE:
            await bot.send_message(
                chat_id=dialog[0].manager_id,
                text=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                     f"отправил вам этот кружочек"
            )

            await bot.send_video_note(
                chat_id=dialog[0].manager_id,
                video_note=message.video_note.file_id,
                reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
            )

    else:
        await message.delete()
