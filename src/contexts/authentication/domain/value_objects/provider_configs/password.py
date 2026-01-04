from src.contexts.authentication.domain.value_objects.provider_configs.base import ProviderConfig


class PasswordProviderConfig(ProviderConfig, forbid_unknown_fields=True):
    ...
