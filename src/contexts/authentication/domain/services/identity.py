from src.contexts.authentication.domain.entities import Identity
from src.contexts.authentication.domain.exceptions import IdentityAlreadyMain


class IdentityDomainService:
    @classmethod
    def set_main(
        cls,
        new: Identity,
        old: Identity | None = None,
    ) -> tuple[Identity, Identity | None]:
        if new.is_main:
            raise IdentityAlreadyMain()
        if old:
            old.is_main = False
        new.is_main = True
        return new, old
