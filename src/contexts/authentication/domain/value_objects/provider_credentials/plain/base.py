from msgspec import Struct


class ProviderPlainCredentials(Struct, frozen=True, omit_defaults=True):
    ...
