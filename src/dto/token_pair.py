from msgspec import Struct

from src.dto import AccessTokenDTO, RefreshTokenDTO
from src.enums import TokenTypes


class TokenPairDTO(Struct):
    access: AccessTokenDTO
    refresh: RefreshTokenDTO
    token_type: TokenTypes
