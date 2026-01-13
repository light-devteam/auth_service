from pydantic import BaseModel


class TelegramProviderCredentials(BaseModel):
    account_id: int
