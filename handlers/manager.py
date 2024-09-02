from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from config.config import bot
from models import User, Dialog
from keyboards.inline.general import ManagerCallbackData
from keyboards.inline.manager_ikb import (manager_menu_ikb, show_all_my_dialogs_ikb, dialog_with_user_ikb,
                                          back_all_dialogs_ikb, approve_search_dialog_ikb, back_manager_menu_ikb)
from state.manager import SearchDialog
from utils.channel import create_link


manager_router = Router()


@manager_router.callback_query(ManagerCallbackData.filter((F.target == 'manager_menu') & (F.action == 'open')))
async def manager_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text(
        text=f"<b>{callback.from_user.full_name}</b>, вы вошли в  <u>панель менеджера!</u>!",
        reply_markup=await manager_menu_ikb()
    )


@manager_router.callback_query(
    ManagerCallbackData.filter((F.target == 'Manager') & (F.action == 'show_all_my_dialogs'))
)
async def show_all_my_dialogs(callback: CallbackQuery, callback_data: ManagerCallbackData, state: FSMContext):
    await state.clear()

    callback_data.manager_id = callback.from_user.id

    dialogs = await Dialog.all(manager_id=callback_data.manager_id)

    await callback.message.edit_text(
        text=f"Список всех моих диалогов:\n"
             f"Всего - {len(dialogs)}",
        reply_markup=await show_all_my_dialogs_ikb(callback_data=callback_data)
    )


@manager_router.callback_query(
    ManagerCallbackData.filter((F.target == 'Manager') & (F.action == 'show_my_link'))
)
async def show_my_link(callback: CallbackQuery, callback_data: ManagerCallbackData, state: FSMContext):
    await state.clear()

    link = await create_link(callback.from_user.id)

    await callback.message.edit_text(
        text=f"Моя пригласительная ссылка:\n"
             f"{link}",
        reply_markup=await back_manager_menu_ikb(callback_data=callback_data)
    )


@manager_router.callback_query(ManagerCallbackData.filter((F.target == 'Manager') & (F.action == 'get_dialog')))
async def get_dialog(callback: CallbackQuery, callback_data: ManagerCallbackData, state: FSMContext):
    await state.clear()

    dialog = await Dialog.get(pk=callback_data.dialog_id)
    user = await User.get(pk=dialog.user_id)

    callback_data.user_id = user.id
    callback_data.manager_id = None

    await callback.message.edit_text(
        text=f"Диалог с {user.tg_first_name} {user.tg_last_name}\n"
             f"Создан: {dialog.created_at}",
        reply_markup=await dialog_with_user_ikb(callback_data=callback_data)
    )


@manager_router.callback_query(ManagerCallbackData.filter((F.target == 'Manager') & (F.action == 'search_dialog')))
async def search_dialog(callback: CallbackQuery, state: FSMContext):

    await state.set_state(SearchDialog.user_id)

    await callback.message.edit_text(
        text=f"Введите id пользователя, чтобы найти с ним диалог",
        reply_markup=await back_all_dialogs_ikb()
    )


@manager_router.message(SearchDialog.user_id)
async def state_search_dialog(message: Message, state: FSMContext):
    await message.delete()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except TelegramBadRequest:
        pass

    dialog = await Dialog.all(user_id=int(message.text))

    callback_data = ManagerCallbackData()

    if dialog:
        if dialog[0].manager_id == message.from_user.id:
            user = await User.get(pk=dialog[0].user_id)

            callback_data.user_id = user.id
            callback_data.dialog_id = dialog[0].id

            await state.clear()

            await message.answer(
                text=f"Диалог с {user.tg_first_name} {user.tg_last_name}\n"
                     f"Создан: {dialog[0].created_at}",
                reply_markup=await dialog_with_user_ikb(callback_data=callback_data)
            )
        else:
            await state.clear()

            await message.answer(
                text=f"Диалог с пользователем(id: {message.text}) не найден.\n"
                     f"Поищем снова?",
                reply_markup=await approve_search_dialog_ikb(callback_data=callback_data)
            )
    else:
        await state.clear()

        await message.answer(
            text=f"Диалог с пользователем(id: {message.text}) не найден.\n"
                 f"Поищем снова?",
            reply_markup=await approve_search_dialog_ikb(callback_data=callback_data)
        )


@manager_router.callback_query(ManagerCallbackData.filter((F.target == 'Manager') & (F.action == 'search_again')))
async def search_again(callback: CallbackQuery, state: FSMContext):

    await state.set_state(SearchDialog.user_id)

    await callback.message.edit_text(
        text=f"Введите id пользователя, чтобы найти с ним диалог",
        reply_markup=await back_all_dialogs_ikb()
    )


@manager_router.callback_query(ManagerCallbackData.filter((F.target == 'Manager') & (F.action == 'send_gift')))
async def send_gift(callback: CallbackQuery):
    await callback.answer("Сервис отправки подарков появится позже")
