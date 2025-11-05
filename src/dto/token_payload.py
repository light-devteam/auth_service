from msgspec import Struct


class TokenPayloadDTO(Struct):
    sub: str
    iat: int
    exp: int
