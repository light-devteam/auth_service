from msgspec import Struct


class AppTokenDTO(Struct):
    token: str
