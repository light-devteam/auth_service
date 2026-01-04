from src.contexts.authentication.domain.value_objects.provider_credentials.base import ProviderCredentials
from src.contexts.authentication.domain.value_objects.credential_fields import Login, Password


class PasswordProviderCredentials(ProviderCredentials):
    login: Login
    password: Password
