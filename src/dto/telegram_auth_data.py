from msgspec import Struct


class TelegramAuthDataDTO(Struct):
    id: int
    first_name: str
    auth_date: int
    hash: str
    last_name: str = ''
    username: str = ''
    photo_url: str = ''
