from src.contexts.authentication.domain.entities import Provider
from src.contexts.authentication.domain.exceptions import ProviderAlreadyActive


class ProviderService:
    def activate(
        self,
        new: Provider,
        old: Provider | None,
    ) -> tuple[Provider, Provider | None]:
        if new.is_active:
            raise ProviderAlreadyActive()
        new.activate()
        if old:
            old.is_active = False
        return new, old
