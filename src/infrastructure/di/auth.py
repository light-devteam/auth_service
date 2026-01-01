from dependency_injector import containers, providers

from src.contexts.authentication.domain.mappers import AccountMapper
from src.contexts.authentication.infrastructure import AccountRepository
from src.contexts.authentication.application.services import AccountApplicationService

from src.contexts.authentication.domain.mappers import ProviderMapper
from src.contexts.authentication.infrastructure import ProviderRepository
from src.contexts.authentication.application.services import ProviderApplicationService

from src.contexts.authentication.domain.mappers import IdentityMapper
from src.contexts.authentication.infrastructure import IdentityRepository
from src.contexts.authentication.application.services import IdentityApplicationService


class AuthContainer(containers.DeclarativeContainer):
    accounts_mapper = providers.Singleton(AccountMapper)
    accounts_repository = providers.Singleton(AccountRepository)
    accounts_service = providers.Singleton(AccountApplicationService)

    provider_mapper = providers.Singleton(ProviderMapper)
    provider_repository = providers.Singleton(ProviderRepository)
    provider_service = providers.Singleton(ProviderApplicationService)

    identity_mapper = providers.Singleton(IdentityMapper)
    identity_repository = providers.Singleton(IdentityRepository)
    identity_service = providers.Singleton(IdentityApplicationService)