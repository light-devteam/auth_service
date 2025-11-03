from pydantic import BaseModel


class CreateAccountSchema(BaseModel):
    telegram_id: int
