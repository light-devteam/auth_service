from src.contexts.authentication.domain.value_objects.provider_credentials.secure.base import ProviderSecureCredentials
from src.contexts.authentication.domain.value_objects.credential_fields import Login, HashedPassword


class PasswordProviderSecureCredentials(ProviderSecureCredentials):
    login: Login
    password: HashedPassword
