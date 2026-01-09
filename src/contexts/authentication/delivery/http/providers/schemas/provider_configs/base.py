from pydantic import BaseModel


class BaseProviderConfig(BaseModel):
    access_token_expire_minutes: int
    refresh_token_expire_days: int
