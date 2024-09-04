from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from config.config import bot
from emuns import UserRole
from models import User, Manager
from keyboards.inline.general import AdminCallbackData
from keyboards.inline.admin_ikb import (admin_menu_ikb, show_all_managers_ikb, confirm_add_manager_ikb,
                                        back_show_all_managers_ikb, confirm_del_manager_ikb)
from keyboards.inline.manager_ikb import notification_new_manager_ikb, manager_menu_ikb
from state.admin import AddManager

admin_router = Router()


@admin_router.message(F.text == '/admin')
async def manager_menu(message: Message, state: FSMContext):
    await message.delete()

    await state.clear()

    user = await User.get(pk=message.from_user.id)

    if user.role != 1:
        try:
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=message.message_id - 1
            )
        except TelegramBadRequest:
            pass

    if user.role == 2:
        await message.answer(
            text=f"<b>{message.from_user.full_name}</b>, вы вошли в  <u>панель менеджера!</u>!",
            reply_markup=await manager_menu_ikb()
        )

    if user.role == 3:
        manager = await Manager.all(user_id=message.from_user.id)
        if manager:
            pass
        else:
            manager = Manager(
                user_id=user.id,
                count_answers=0
            )
            await manager.save()

        await message.answer(
            text=f"<b>{message.from_user.full_name}</b>, вы вошли в  <u>панель администратора!</u>!",
            reply_markup=await admin_menu_ikb()
        )


@admin_router.callback_query(AdminCallbackData.filter((F.target == 'admin_menu') & (F.action == 'open')))
async def admin_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text=f"<b>{callback.from_user.full_name}</b>, вы вошли в  <u>панель администратора!</u>!",
        reply_markup=await admin_menu_ikb()
    )


@admin_router.callback_query(AdminCallbackData.filter((F.target == 'Admin') & (F.action == 'show_all_managers')))
async def show_all_managers(callback: CallbackQuery, callback_data: AdminCallbackData, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text="Список всех менеджеров\n"
             "(возможно удаление и добавлние)",
        reply_markup=await show_all_managers_ikb(callback_data=callback_data)
    )


@admin_router.callback_query(AdminCallbackData.filter((F.target == 'Admin') & (F.action == 'add_manager')))
async def add_manager(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddManager.user_id)
    await callback.message.edit_text(
        text="Введите id пользователя, которого нужно перевести в менеджеры",
        reply_markup=await back_show_all_managers_ikb()
    )


@admin_router.message(AddManager.user_id)
async def state_add_manager(message: Message, state: FSMContext):
    await message.delete()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except TelegramBadRequest:
        pass

    user = await User.get(pk=int(message.text))

    if user:
        if user.role == 1:
            await state.update_data(user_id=user.id)

            await message.answer(
                text=f"Вы действительно хотите перевести пользователя @{user.tg_username}\n"
                     f"({user.tg_first_name} {user.tg_last_name}) в менеджеры?",
                reply_markup=await confirm_add_manager_ikb()
            )

        if user.role == 2:
            await state.set_state(AddManager.user_id)

            await message.answer(
                text="Пользователь с таким id уже является менеджером!\n"
                     "Попробуйте еще раз.",
                reply_markup=await back_show_all_managers_ikb()
            )

        if user.role == 3:
            await state.set_state(AddManager.user_id)

            await message.answer(
                text="Пользователь с таким id уже является администратором!\n"
                     "Попробуйте еще раз.",
                reply_markup=await back_show_all_managers_ikb()
            )

    else:
        await state.set_state(AddManager.user_id)

        await message.answer(
            text="Пользователь с таким id не найден!\n"
                 "Попробуйте еще раз.",
            reply_markup=await back_show_all_managers_ikb()
        )


@admin_router.callback_query(AdminCallbackData.filter((F.target == 'Admin') & (F.action == 'confirm_add')))
async def confirm_add_manager(callback: CallbackQuery, callback_data: AdminCallbackData, state: FSMContext):
    if callback_data.details == "no":
        await state.clear()

        await callback.message.edit_text(
            text="Список всех менеджеров\n"
                 "(возможно удаление и добавлние)",
            reply_markup=await show_all_managers_ikb(callback_data=callback_data)
        )
    if callback_data.details == "yes":
        data = await state.get_data()

        user = await User.get(pk=data['user_id'])
        user.role = UserRole.ADMIN
        await user.save()

        manager = Manager(
            user_id=user.id,
            count_answers=0
        )
        await manager.save()

        await callback.answer("Пользователь переведен в менеджеры!")

        await bot.send_message(
            chat_id=user.id,
            text="Поздравляю!\n"
                 "Вас перевели в менеджеры!\n\n"
                 "Для входа в меню менеджера введите /admin",
            reply_markup=await notification_new_manager_ikb()
        )

        await state.clear()

        await callback.message.edit_text(
            text="Список всех менеджеров\n"
                 "(возможно удаление и добавлние)",
            reply_markup=await show_all_managers_ikb(callback_data=callback_data)
        )


@admin_router.callback_query(AdminCallbackData.filter((F.target == 'Admin') & (F.action == 'get_manager')))
async def get_manager(callback: CallbackQuery, callback_data: AdminCallbackData):
    manager = await User.get(pk=callback_data.manager_id)

    count_dialogs = await Manager.all(user_id=manager.id)

    await callback.message.edit_text(
        text=f"Менеджер @{manager.tg_username} ({manager.tg_first_name}{manager.tg_last_name})\n"
             f"Общее колличество диалогов: {count_dialogs[0].count_answers}",
        reply_markup=await back_show_all_managers_ikb()
    )


@admin_router.callback_query(AdminCallbackData.filter((F.target == 'Admin') & (F.action == 'del_manager')))
async def del_manager(callback: CallbackQuery, callback_data: AdminCallbackData):
    manager = await User.get(pk=callback_data.manager_id)

    await callback.message.edit_text(
        text=f"Вы действительно хотите перевести @{manager.tg_username} "
             f"({manager.tg_first_name}{manager.tg_last_name}) в пользователи?",
        reply_markup=await confirm_del_manager_ikb(callback_data=callback_data)
    )


@admin_router.callback_query(AdminCallbackData.filter((F.target == 'Admin') & (F.action == 'confirm_del')))
async def confirm_del(callback: CallbackQuery, callback_data: AdminCallbackData):
    manager = await User.get(pk=callback_data.manager_id)
    manager_tabl = await Manager.get(user_id=callback_data.manager_id)

    manager.role = UserRole.USER
    await manager.save()

    if manager_tabl:
        await manager_tabl.delete()

    await callback.answer("Пользователь удален из менеджеров!")

    await callback.message.edit_text(
        text="Список всех менеджеров\n"
             "(возможно удаление и добавлние)",
        reply_markup=await show_all_managers_ikb(callback_data=callback_data)
    )