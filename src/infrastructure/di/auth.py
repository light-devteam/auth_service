from dependency_injector import containers, providers

from src.contexts.authentication.domain import mappers, services as domain_services
from src.contexts.authentication import infrastructure
from src.contexts.authentication.application import services
from src.contexts.authentication import AuthenticationContext


class AuthContainer(containers.DeclarativeContainer):
    accounts_mapper = providers.Singleton(mappers.AccountMapper)
    accounts_repository = providers.Singleton(infrastructure.AccountRepository)
    accounts_service = providers.Singleton(services.AccountApplicationService)

    provider_domain_service = providers.Singleton(domain_services.ProviderService)
    provider_mapper = providers.Singleton(mappers.ProviderMapper)
    provider_repository = providers.Singleton(infrastructure.ProviderRepository)
    provider_service = providers.Singleton(services.ProviderApplicationService)

    identity_mapper = providers.Singleton(mappers.IdentityMapper)
    identity_repository = providers.Singleton(infrastructure.IdentityRepository)
    identity_service = providers.Singleton(services.IdentityApplicationService)

    session_mapper = providers.Singleton(mappers.SessionMapper)
    session_repository = providers.Singleton(infrastructure.SessionRepository)
    session_service = providers.Singleton(services.SessionApplicationService)

    refresh_token_mapper = providers.Singleton(mappers.RefreshTokenMapper)
    refresh_token_repository = providers.Singleton(infrastructure.RefreshTokenRepository)

    access_token_jwt_issuer = providers.Singleton(infrastructure.JWTAccessTokenIssuer)
    refresh_token_b64_issuer = providers.Singleton(infrastructure.Base64RefreshTokenIssuer)

    context = providers.Singleton(AuthenticationContext)
