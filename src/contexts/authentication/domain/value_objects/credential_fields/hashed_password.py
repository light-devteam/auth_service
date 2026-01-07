from typing import Self

import bcrypt

from src.contexts.authentication.domain.value_objects.credential_fields.password import Password


class HashedPassword(str):
    def __new__(cls, value: Password) -> Self:
        if not isinstance(value, Password):
            raise TypeError('Only type Password supported!')
        hashed_value = bcrypt.hashpw(value, bcrypt.gensalt())
        return super().__new__(cls, hashed_value.decode('utf-8'))

    def __str__(self) -> str:
        return 'hashed'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__str__()})'
