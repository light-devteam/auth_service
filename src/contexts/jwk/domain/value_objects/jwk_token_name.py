from typing import Self


class JWKTokenName(str):
    _max_length = 255

    def __new__(cls, value: str) -> Self:
        if len(value) > cls._max_length:
            raise ValueError(f'Length cannot be more than {cls._max_length}')
        return super().__new__(cls, value)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__str__()})'
