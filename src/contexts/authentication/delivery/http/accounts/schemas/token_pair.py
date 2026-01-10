from pydantic import BaseModel

from src.contexts.authentication.delivery.http.accounts.schemas.access_token import AccessToken
from src.contexts.authentication.delivery.http.accounts.schemas.refresh_token import RefreshToken


class TokenPair(BaseModel):
    access: AccessToken
    refresh: RefreshToken
