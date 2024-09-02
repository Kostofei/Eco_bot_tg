from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from config.config import bot
from models import User, Dialog
from keyboards.inline.general import DialogCallbackData, ManagerCallbackData
from keyboards.inline.manager_ikb import back_dialog_with_user_ikb
from keyboards.inline.dialog_ikb import answer_for_user_dialog_ikb
from state.dialog import DialogForUserState, DialogForManagerState

dialog_router = Router()


@dialog_router.callback_query(ManagerCallbackData.filter((F.target == 'Dialog') & (F.action == 'get_sms_for_user')))
async def get_sms_for_user(callback: CallbackQuery, callback_data: ManagerCallbackData, state: FSMContext):
    user = await User.get(pk=callback_data.user_id)

    if callback_data.details == "mng_menu":

        await state.update_data(dialog_id=callback_data.dialog_id)
        await state.update_data(details=callback_data.details)

        await state.set_state(DialogForUserState.sms)

        await callback.message.edit_text(
            text=f"Введите сообщение для {user.tg_first_name} {user.tg_last_name}",
            reply_markup=await back_dialog_with_user_ikb(callback_data=callback_data)
        )


@dialog_router.callback_query(DialogCallbackData.filter((F.target == 'Dialog') & (F.action == 'answer_for_user')))
async def answer_for_user(callback: CallbackQuery, callback_data: ManagerCallbackData, state: FSMContext):
    dialog = await Dialog.get(pk=callback_data.dialog_id)
    user = await User.get(pk=dialog.user_id)

    await state.update_data(dialog_id=callback_data.dialog_id)
    await state.set_state(DialogForUserState.sms)

    await callback.message.answer(
        text=f"Введите сообщение для {user.tg_first_name} {user.tg_last_name}",
    )


@dialog_router.message(DialogForUserState.sms)
async def state_sms_for_user(message: Message, state: FSMContext):
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except TelegramBadRequest:
        pass

    data = await state.get_data()
    dialog = await Dialog.get(pk=data['dialog_id'])
    manager = await User.get(pk=dialog.manager_id)

    await state.clear()

    if message.content_type == ContentType.TEXT:
        await bot.send_message(
            chat_id=dialog.user_id,
            text=f"Консультант {manager.first_name}:\n\n"
                 f"{message.text}"
        )

    if message.content_type == ContentType.PHOTO:
        await bot.send_message(
            chat_id=dialog.user_id,
            text=f"Консультант {manager.first_name}:\n\n"
        )

        await bot.send_photo(
            chat_id=dialog.user_id,
            photo=message.photo[0].file_id
        )

    if message.content_type == ContentType.DOCUMENT:
        await bot.send_message(
            chat_id=dialog.user_id,
            text=f"Консультант {manager.first_name}:\n\n"
        )

        await bot.send_document(
            chat_id=dialog.user_id,
            document=message.document.file_id
        )

    if message.content_type == ContentType.VIDEO:
        await bot.send_message(
            chat_id=dialog.user_id,
            text=f"Консультант {manager.first_name}:\n\n"
        )

        await bot.send_video(
            chat_id=dialog.user_id,
            video=message.video.file_id
        )

    if message.content_type == ContentType.VOICE:
        await bot.send_message(
            chat_id=dialog.user_id,
            text=f"Консультант {manager.first_name}:\n\n",
        )

        await bot.send_voice(
            chat_id=dialog.user_id,
            voice=message.voice.file_id
        )

    if message.content_type == ContentType.VIDEO_NOTE:
        await bot.send_message(
            chat_id=dialog.user_id,
            text=f"Консультант {manager.first_name}:\n\n"
        )

        await bot.send_video_note(
            chat_id=dialog.user_id,
            video_note=message.video_note.file_id
        )


@dialog_router.callback_query(DialogCallbackData.filter((F.target == 'Dialog') & (F.action == 'answer_for_manager')))
async def answer_for_manager(callback: CallbackQuery, callback_data: DialogCallbackData, state: FSMContext):

    await state.update_data(dialog_id=callback_data.dialog_id)
    await state.set_state(DialogForManagerState.sms)

    await callback.message.answer(
        text=f"Введите сообщение вашему закрепленному менеджеру."
    )


@dialog_router.message(DialogForManagerState.sms)
async def state_sms_for_manager(message: Message, state: FSMContext, callback_data: DialogCallbackData = None):
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except TelegramBadRequest:
        pass

    data = await state.get_data()
    dialog = await Dialog.get(pk=data['dialog_id'])
    user = await User.get(pk=dialog.user_id)

    await state.clear()

    if callback_data is None:
        callback_data = DialogCallbackData(
            dialog_id=dialog.id
        )

    if message.content_type == ContentType.TEXT:

        await bot.send_message(
            chat_id=dialog.manager_id,
            text=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                 f"отправил вам сообщение:\n\n"
                 f"{message.text}",
            reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
        )

    if message.content_type == ContentType.PHOTO:

        await bot.send_photo(
            chat_id=dialog.manager_id,
            photo=message.photo[0].file_id,
            caption=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                    f"отправил вам это изображение",
            reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
        )

    if message.content_type == ContentType.DOCUMENT:

        await bot.send_document(
            chat_id=dialog.manager_id,
            document=message.document.file_id,
            caption=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                    f"отправил вам этот документ",
            reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
        )

    if message.content_type == ContentType.VIDEO:

        await bot.send_video(
            chat_id=dialog.manager_id,
            video=message.video.file_id,
            caption=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                    f"отправил вам это видео",
            reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
        )

    if message.content_type == ContentType.VOICE:

        await bot.send_voice(
            chat_id=dialog.manager_id,
            voice=message.voice.file_id,
            caption=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                    f"отправил вам это голосовое сообщение",
            reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
        )

    if message.content_type == ContentType.VIDEO_NOTE:
        await bot.send_message(
            chat_id=dialog.manager_id,
            text=f"Пользователь {user.tg_first_name} {user.tg_last_name}\n"
                 f"отправил вам этот кружочек"
        )

        await bot.send_video_note(
            chat_id=dialog.manager_id,
            video_note=message.video_note.file_id,
            reply_markup=await answer_for_user_dialog_ikb(callback_data=callback_data)
        )
