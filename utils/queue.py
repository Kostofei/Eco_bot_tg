import asyncio
from config.config import bot
from datetime import datetime
from aiogram.types import CallbackQuery
from keyboards.inline.general import UserCallbackData
from keyboards.inline.admin_ikb import answer_for_user_ikb
from keyboards.inline.start_ikb import main_menu_ikb
from models import User, Dialog, Manager
from emuns import UserRole


async def queue(callback_data: UserCallbackData, callback: CallbackQuery = None):
    user = await User.get(pk=callback_data.user_id)
    user_dialogs = await Dialog.all(user_id=user.id)
    text_for_manager = ""
    text_for_user = ""

    if callback_data.target == "Gift":
        gift = callback_data.gift
        callback_data.gift = None
        text_for_manager = f"Пользователь @{user.tg_username} ({user.tg_first_name} {user.tg_username})" \
                           f" получил подарок:\n" \
                           f"🎁 {gift} 🎁\n"

    if callback_data.target == "Mini_course":
        text = callback_data.details
        callback_data.details = None
        text_for_manager = f"Пользователь @{user.tg_username} ({user.tg_first_name} {user.tg_username})\n" \
                           f"{text}"

    if callback_data.target == "Calculation":
        text = callback_data.details
        callback_data.details = None
        text_for_manager = f"Пользователь @{user.tg_username} ({user.tg_first_name} {user.tg_username})\n" \
                           f"{text}"

        text_for_user = 'В ближайшее время тебе будет выслан твой "Расчет индивидуальной экономии."\n' \
                        'Для большей эффективности, направляю тебя на личного консультанта.\n' \
                        'Он вышлет тебе вместе с расчетом 🎁БОНУС🎁'

    if callback_data.target == "Question":
        text_for_manager = f"Пользователю @{user.tg_username} ({user.tg_first_name} {user.tg_username})" \
                           f" нужна консультация"

        text_for_user = ("Ваш запрос принят.\n "
                         "Для большей эффективности направляю тебя на личного консультанта\n "
                         "Скоро он подключится и ответит на твои вопросы.")

    if callback_data.target == "Webinar":
        text_for_manager = f"Пользователь @{user.tg_username} ({user.tg_first_name} {user.tg_username})" \
                           f" записался на вэбинар"

        text_for_user = ("Ваш запрос принят.\n "
                         "О времени ближайшего вэбинара мы вам сообщим дополнительно")

    if callback_data.target == "Order":
        text = callback_data.details
        callback_data.details = None
        text_for_manager = f"Пользователю @{user.tg_username} ({user.tg_first_name} {user.tg_username})\n" \
                           f"{text}"

        text_for_user = "Ваш запрос принят.\n" \
                        "Для большей эффективности направляю тебя на личного консультанта\n" \
                        "Он поможет с заказом."

    if len(text_for_user) > 0:
        await callback.message.delete()

        await callback.message.answer(
            text=text_for_user,
            reply_markup=await main_menu_ikb()
        )
        # Если есть смс, для юзера, то отправляем

    if user_dialogs:
        # Если диалог уже существует

        for user_dialog in user_dialogs:
            if user_dialog and user_dialog.manager_id:
                admin = await User.get(pk=user_dialog.manager_id)

                callback_data.user_id = user.id
                callback_data.dialog_id = user_dialog.id

                await bot.send_message(
                    chat_id=admin.id,
                    text=text_for_manager,
                    reply_markup=await answer_for_user_ikb(callback_data=callback_data)
                )
                # Отправляет смс менеджеру
                break

    else:
        # Если диалога еще нет

        dialog = Dialog(
            user_id=user.id,
            created_at=datetime.now(),
            is_active=True
        )
        await dialog.save()
        # Создали диалог

        max_count_answers = 0
        managers = await Manager.all()

        for manager in managers:
            if manager.count_answers > max_count_answers:
                max_count_answers = manager.count_answers
            else:
                continue
        # Записываем максимальное колличество диалогов у менеджеров

        count_admin_dialogs = 0

        while 1:

            if count_admin_dialogs <= (max_count_answers + 1):
                # Ограничение, чтоб не выходить за максимальное колличество диалогов у менеджеров

                admins = await User.all(role=UserRole.ADMIN)

                super_admins = await User.all(role=UserRole.SUPER_ADMIN)

                for super_admin in super_admins:
                    admins.append(super_admin)

                for admin in admins:
                    this_manager = await Manager.all(user_id=admin.id)

                    if this_manager[0].count_answers == count_admin_dialogs:
                        callback_data.user_id = user.id
                        callback_data.dialog_id = dialog.id

                        await bot.send_message(
                            chat_id=admin.id,
                            text=text_for_manager,
                            reply_markup=await answer_for_user_ikb(callback_data=callback_data),
                            disable_web_page_preview=True)
                # Одновременно отправляет смс всем менеджерам с наименьшим колличеством диалогов

                await asyncio.sleep(60)
                # Даем менеджерам время взять в работу

                check_dialog = await Dialog.get(pk=dialog.id)
                if check_dialog.manager_id:
                    # Если менеджер закреплен
                    break

                count_admin_dialogs += 1
                # Если никто не взял в работу, переходим к менеджерам у которых диалогов больше.

            else:
                over_check_dialog = await Dialog.get(pk=dialog.id)
                if not over_check_dialog.manager_id:
                    # Если менеджеры закончились и никто не взял в работу
                    break

        # Цикл отработал!
