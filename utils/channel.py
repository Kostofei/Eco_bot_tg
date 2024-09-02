from aiogram.enums import ChatMemberStatus
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.deep_linking import create_start_link
from config.config import bot
from keyboards.inline.general import UserCallbackData
from keyboards.inline.gift_ikb import check_subscribe_ikb
from schemas import ChatDetail


async def is_subscription(callback: CallbackQuery, callback_data: UserCallbackData):
    subscription = await is_chat_member(
        chat_id=callback_data.chat_id,
        user_id=callback_data.user_id
    )

    if not subscription:
        try:
            chat_name = await get_chat_name(chat_id=callback_data.chat_id)
            callback_data.details = chat_name.invite_link
            await callback.answer(text="Вы не подписаны на канал!")
            await callback.message.answer(
                text=f"💕 Проделана большая работа и все, что я даю - это бесплатно\n"
                     f'🤝 Твоей благодарностью будет подписка на канал "ГАРМОНИЯ ЖИЗНИ"',
                reply_markup=await check_subscribe_ikb(callback_data=callback_data),
                disable_web_page_preview=True
            )
        except TelegramBadRequest:
            pass
    else:
        return True


async def is_chat_member(chat_id, user_id: int) -> bool:
    check_member = await bot.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    if check_member.status == ChatMemberStatus.MEMBER or check_member.status == ChatMemberStatus.ADMINISTRATOR or \
            check_member.status == ChatMemberStatus.CREATOR:
        return True
    return False


async def get_chat_name(chat_id: int) -> ChatDetail:
    chat_name = await bot.get_chat(
        chat_id=chat_id,
        request_timeout=1
    )
    data = ChatDetail(
        name=chat_name.title,
        invite_link=chat_name.invite_link
    )
    return data


async def create_link(manger_id) -> str:
    link = await create_start_link(
        bot=bot,
        payload=str(manger_id),
        encode=True
    )
    return link
