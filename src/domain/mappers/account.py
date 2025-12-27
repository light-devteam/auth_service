from typing import Mapping

from src.domain.entities import Account
from src.domain.value_objects import AccountID


class AccountMapper:
    def to_entity(self, raw: Mapping) -> Account:
        return Account(id=AccountID(raw['id']))
