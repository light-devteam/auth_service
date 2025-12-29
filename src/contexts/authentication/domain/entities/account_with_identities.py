from src.domain.entities import Account
from src.contexts.authentication.domain.entities.identity import Identity
from src.contexts.authentication.domain.exceptions import (
    MainIdentityAlreadySet,
    IdentityForProviderAlreadyExists,
)


class AccountWithIdentities:
    account: Account
    identities: list[Identity] = []

    def add_identity(self, identity: Identity) -> None:
        if any(i.provider_id == identity.provider_id for i in self.identities):
            raise IdentityForProviderAlreadyExists()
        if identity.is_main:
            if any(i.is_main for i in self.identities):
                raise MainIdentityAlreadySet()
        self.identities.append(identity)
