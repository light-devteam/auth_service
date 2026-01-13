from pydantic import BaseModel

from src.contexts.authentication.delivery.http.auth.schemas.access_token import AccessToken
from src.contexts.authentication.delivery.http.auth.schemas.refresh_token import RefreshToken


class TokenPair(BaseModel):
    access: AccessToken
    refresh: RefreshToken
