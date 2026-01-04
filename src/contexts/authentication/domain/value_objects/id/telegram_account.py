from typing import Self


class TelegramAccountID(int):
    def __new__(cls, value: int) -> Self:
        INT64_MAX = 9223372036854775807
        if value < 0 or value > INT64_MAX:
            raise ValueError(f'Telegram account id must be 64-bit int (0 to {INT64_MAX})')
        return super().__new__(cls, value)
