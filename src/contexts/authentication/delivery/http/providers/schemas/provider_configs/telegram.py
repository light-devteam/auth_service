from pydantic import BaseModel


class TelegramProviderConfig(BaseModel):
    bot_id: int
