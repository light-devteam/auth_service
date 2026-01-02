from src.domain.entities import Account
from src.contexts.authentication.domain.entities.identity import Identity
from src.contexts.authentication.domain.exceptions import IdentityForProviderAlreadyExists


class AccountWithIdentities:
    account: Account
    identities: list[Identity] = []

    def add_identity(self, identity: Identity) -> None:
        if any(i.provider_id == identity.provider_id for i in self.identities):
            raise IdentityForProviderAlreadyExists()
        self.identities.append(identity)
