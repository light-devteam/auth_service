from pydantic import BaseModel

from src.enums import TokenTypes
from src.schemas.sessions.access_token import AccessTokenSchema
from src.schemas.sessions.refresh_token import RefreshTokenSchema


class TokenPairSchema(BaseModel):
    access: AccessTokenSchema
    refresh: RefreshTokenSchema
    token_type: TokenTypes
