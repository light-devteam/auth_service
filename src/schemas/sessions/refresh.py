from pydantic import BaseModel


class RefreshSessionSchema(BaseModel):
    refresh_token: str
