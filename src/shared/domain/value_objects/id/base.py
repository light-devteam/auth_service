from typing import Self
from uuid import UUID, uuid4


class BaseID(UUID):
    def __init__(self, value: UUID | int | bytes | str | None = None) -> None:
        if value is None:
            super().__init__(int=uuid4().int)
        elif isinstance(value, UUID):
            super().__init__(int=value.int)
        elif isinstance(value, int):
            super().__init__(int=value)
        elif isinstance(value, str):
            super().__init__(hex=value)
        elif isinstance(value, bytes):
            super().__init__(bytes=value)
        else:
            super().__init__(str(value))

    @classmethod
    def generate(cls) -> Self:
        return cls()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self})'
