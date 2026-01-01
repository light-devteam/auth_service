from dependency_injector import containers, providers

from src.contexts.jwk.domain.mappers import JWKMapper
from src.contexts.jwk.infrastructure import JWKRepository
from src.contexts.jwk.application.services import JWKApplicationService
from src.contexts.jwk.domain.services import JWKTokenService


class JWKContainer(containers.DeclarativeContainer):
    mapper = providers.Singleton(JWKMapper)
    repository = providers.Singleton(JWKRepository)
    domain_service = providers.Singleton(JWKTokenService)
    service = providers.Singleton(JWKApplicationService)
