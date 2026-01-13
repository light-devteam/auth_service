from pydantic import BaseModel


class RefreshTokensRequest(BaseModel):
    refresh_token: str
