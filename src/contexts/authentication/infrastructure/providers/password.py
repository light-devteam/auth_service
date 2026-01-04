from src.contexts.authentication.domain.value_objects import PasswordProviderCredentials
from src.domain.value_objects import AccountID
from src.contexts.authentication.domain.entities import Session
from src.contexts.authentication.domain.providers import IProvider


class PasswordProvider(IProvider):
    async def authenticate(
        self,
        account_id: AccountID,
        credentials: PasswordProviderCredentials,
    ) -> Session:
        ...
