from pydantic import BaseModel


class ChatDetail(BaseModel):
    name: str
    invite_link: str
