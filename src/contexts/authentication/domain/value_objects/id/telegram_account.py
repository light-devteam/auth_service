from typing import Self


class TelegramAccountID(str):
    INT64_MAX = 9223372036854775807

    def __new__(cls, value: int | str) -> Self:
        if isinstance(value, str):
            value = int(value)
        if value < 1 or value > cls.INT64_MAX:
            raise ValueError(f'Telegram account id must be 64-bit int (1 to {cls.INT64_MAX})')
        value = str(value)
        return super().__new__(cls, value)
