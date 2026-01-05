from typing import Self


class TelegramAccountID(int):
    INT64_MAX = 9223372036854775807

    def __new__(cls, value: int) -> Self:
        if value < 1 or value > cls.INT64_MAX:
            raise ValueError(f'Telegram account id must be 64-bit int (1 to {cls.INT64_MAX})')
        return super().__new__(cls, value)
