from msgspec import Struct


class JWKSDTO(Struct):
    keys: list[dict]
