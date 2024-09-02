from config.config import bot
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline.general import UserCallbackData, DialogCallbackData
from keyboards.inline.dialog_ikb import answer_for_manager_ikb
from models import Dialog, Manager, User
from utils.queue import queue
from state.dialog import DialogForUserState

question_router = Router()


@question_router.callback_query(UserCallbackData.filter((F.target == "Question") & (F.action == "main")))
async def question(callback: CallbackQuery, callback_data: UserCallbackData):
    callback_data.user_id = callback.from_user.id
    await queue(callback=callback, callback_data=callback_data)


@question_router.callback_query(UserCallbackData.filter((F.target == "Question") & (F.action == "gift_user_second")))
async def gift_user(callback: CallbackQuery):
    await callback.message.delete()


@question_router.callback_query(UserCallbackData.filter((F.target == "Question") & (F.action == "gift_user")))
async def gift_user(callback: CallbackQuery, callback_data: UserCallbackData):

    dialog_id = callback_data.dialog_id
    dialog = await Dialog.get(pk=dialog_id)

    if dialog.manager_id:
        if dialog.manager_id == callback.from_user.id:

            user = await User.get(pk=dialog.user_id)
            manager = await User.get(pk=dialog.manager_id)

            callback_data = DialogCallbackData(
                dialog_id=dialog.id,
                details="question"
            )

            await bot.send_message(
                chat_id=dialog.user_id,
                text=f"{user.tg_first_name}, ваш закрепленный менеджер {manager.first_name}\n"
                     f"Вы можете задать ему любой вопрос.",
                reply_markup=await answer_for_manager_ikb(callback_data=callback_data)
            )

        else:
            await callback.answer(text="Пользователь уже закреплен за другим менеджером!")
    else:
        dialog.manager_id = callback.from_user.id
        await dialog.save()

        manager_answers = await Manager.all(user_id=callback.from_user.id)
        manager_answers[0].count_answers += 1
        await manager_answers[0].save()

        await callback.answer(text="Пользователь закреплен за вами!")

        user = await User.get(pk=dialog.user_id)
        manager = await User.get(pk=dialog.manager_id)

        callback_data = DialogCallbackData(
            dialog_id=dialog.id,
            details="question"
        )

        await bot.send_message(
            chat_id=dialog.user_id,
            text=f"{user.tg_first_name}, ваш закрепленный менеджер {manager.first_name}\n"
                 f"Вы можете задать ему любой вопрос.",
            reply_markup=await answer_for_manager_ikb(callback_data=callback_data)
        )


@question_router.callback_query(UserCallbackData.filter((F.target == "Question") & (F.action == "survey_user")))
async def survey_user(callback: CallbackQuery, callback_data: UserCallbackData, state: FSMContext):

    dialog_id = callback_data.dialog_id
    dialog = await Dialog.get(pk=dialog_id)

    if dialog.manager_id:
        if dialog.manager_id == callback.from_user.id:
            await callback.answer(text="Не забудьте отправить опрос!")

            user = await User.get(pk=dialog.user_id)

            await state.update_data(dialog_id=dialog_id)
            await state.set_state(DialogForUserState.sms)

            await callback.message.answer(
                text=f"Пришлите опрос для {user.tg_first_name} {user.tg_last_name}"
            )

        else:
            await callback.answer(text="Пользователь уже закреплен за другим менеджером!")
    else:
        dialog.manager_id = callback.from_user.id
        await dialog.save()

        manager_answers = await Manager.all(user_id=callback.from_user.id)
        manager_answers[0].count_answers += 1
        await manager_answers[0].save()

        await callback.answer(text="Пользователь закреплен за вами!\n"
                                   "Не забудьте отправить опрос!")

        user = await User.get(pk=dialog.user_id)

        await state.update_data(dialog_id=dialog_id)
        await state.set_state(DialogForUserState.sms)

        await callback.message.answer(
            text=f"Пришлите опрос для {user.tg_first_name} {user.tg_last_name}"
        )

'''
@question_router.message(DialogForUserState.sms)
async def state_sms_for_user(message: Message, state: FSMContext, callback_data: DialogCallbackData = None):
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

    if callback_data is None:
        callback_data = DialogCallbackData(
            dialog_id=dialog.id
        )

    if message.content_type == ContentType.TEXT:
        await bot.send_message(
            chat_id=dialog.user_id,
            text=f"Консультант {manager.first_name}:\n\n"
                 f"{message.text}",
            reply_markup=await answer_for_manager_ikb(callback_data=callback_data)
        )
'''


@question_router.callback_query(UserCallbackData.filter((F.target == "Question") & (F.action == "take_user")))
async def take_user(callback: CallbackQuery, callback_data: UserCallbackData, state: FSMContext):

    dialog = await Dialog.get(pk=callback_data.dialog_id)

    if dialog.manager_id:
        if dialog.manager_id == callback.from_user.id:

            user = await User.get(pk=dialog.user_id)

            await state.update_data(dialog_id=dialog.id)
            await state.set_state(DialogForUserState.sms)

            await callback.message.answer(
                text=f"Введите сообщение для {user.tg_first_name} {user.tg_last_name}",
            )

        else:
            await callback.answer(text="Пользователь уже закреплен за другим менеджером!")

    else:
        dialog.manager_id = callback.from_user.id
        await dialog.save()

        manager_answers = await Manager.all(user_id=callback.from_user.id)
        manager_answers[0].count_answers += 1
        await manager_answers[0].save()

        await callback.answer(text="Пользователь закреплен за вами!")

        user = await User.get(pk=dialog.user_id)

        await state.update_data(dialog_id=dialog.id)
        await state.set_state(DialogForUserState.sms)

        await callback.message.answer(
            text=f"Введите сообщение для {user.tg_first_name} {user.tg_last_name}",
        )
