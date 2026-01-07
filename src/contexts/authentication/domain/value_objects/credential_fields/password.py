from typing import Self


class Password(bytes):
    _min_length = 6
    _max_length = 72

    def __new__(cls, value: str | bytes) -> Self:
        if isinstance(value, str):
            value = value.encode('utf-8')
        if len(value) < cls._min_length:
            raise ValueError(f'Length cannot be less than {cls._min_length} bytes')
        if len(value) > cls._max_length:
            raise ValueError(f'Length cannot be more than {cls._max_length} bytes')
        return super().__new__(cls, value)

    def __str__(self) -> str:
        return '*' * self._min_length

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__str__()})'
