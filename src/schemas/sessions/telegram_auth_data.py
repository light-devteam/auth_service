from typing import Optional

from pydantic import BaseModel


class TelegramAuthDataSchema(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = ''
    username: Optional[str] = ''
    photo_url: Optional[str] = ''
    auth_date: int
    hash: str
