from src.contexts.authentication.domain.value_objects.provider_credentials.plain.base import ProviderPlainCredentials
from src.contexts.authentication.domain.value_objects.credential_fields import Login, Password


class PasswordProviderPlainCredentials(ProviderPlainCredentials):
    login: Login
    password: Password
