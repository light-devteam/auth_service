from dependency_injector import containers, providers

from src.infrastructure.di.infrastructure import InfrastructureContainer
from src.infrastructure.di.system import SystemContainer
from src.infrastructure.di.jwk import JWKContainer
from src.infrastructure.di.auth import AuthContainer
from src.infrastructure.di.providers import ProvidersContainer


class DIContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            'src.bootstrap',

            'src.contexts.system.application',
            'src.contexts.system.delivery',

            'src.contexts.jwk.domain.value_objects',
            'src.contexts.jwk.infrastructure.repositories',
            'src.contexts.jwk.application',
            'src.contexts.jwk.delivery.http',

            'src.contexts.authentication.infrastructure.repositories',
            'src.contexts.authentication.infrastructure.token_managers',
            'src.contexts.authentication.application',
            'src.contexts.authentication.delivery.http',
        ],
        modules=[
            'src.contexts.jwk.context',
            'src.contexts.authentication.context',
        ]
    )

    infrastructure = providers.Container(InfrastructureContainer)
    system = providers.Container(
        SystemContainer,
        postgres_uow=infrastructure.postgres_uow,
        redis_session=infrastructure.redis_session,
    )
    jwk = providers.Container(JWKContainer)
    auth = providers.Container(AuthContainer)
    auth_providers = providers.Container(ProvidersContainer)
