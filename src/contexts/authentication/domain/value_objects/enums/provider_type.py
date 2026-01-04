from enum import StrEnum


class ProviderType(StrEnum):
    UNKNOWN = 'unknown'
    PASSWORD = 'password'
    TELEGRAM = 'telegram'
