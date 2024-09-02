from pydantic import BaseModel


class BotSchema(BaseModel):
    TOKEN: str


class ConfigSchema(BaseModel):
    BOT: BotSchema
    DATABASE: str
    CHAT_ID: int
