from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Главное меню"
        ),
        BotCommand(
            command="gift",
            description="Получить подарок"
        ),
        BotCommand(
            command="catalogue",
            description="Каталог"
        )
    ]

    await bot.set_my_commands(
        commands=commands,
        language_code='ru'
    )
