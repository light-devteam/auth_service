from typing import Self

from msgspec import Struct

from src.domain.value_objects.id import AccountID


class Account(Struct):
    id: AccountID

    @classmethod
    def create(cls) -> Self:
        return Account(id=AccountID.generate())
