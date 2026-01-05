from src.contexts.authentication.domain.value_objects.provider_credentials.base import ProviderCredentials
from src.contexts.authentication.domain.value_objects.credential_fields import Login, Password


class PasswordProviderCredentials(ProviderCredentials):
    login: str
    password: str

    def __post_init__(self) -> None:
        Login(self.login)
        Password(self.password)
