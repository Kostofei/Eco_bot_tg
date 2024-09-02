import os
from json import load
from pathlib import Path
from schemas import ConfigSchema
from aiogram import Bot, Dispatcher

BASE_DIR = Path(__file__).resolve().parents[1]


def load_config() -> ConfigSchema:
    with open(os.path.join(BASE_DIR, "config.json"), "r", encoding="utf-8") as file:
        return ConfigSchema(**load(file))


CONFIG: ConfigSchema = load_config()

bot = Bot(
    token=CONFIG.BOT.TOKEN,
    parse_mode='HTML'
)
dp = Dispatcher(bot=bot)
