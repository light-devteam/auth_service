import inspect
import uuid
from datetime import timezone, datetime
from typing import Type
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.contexts.authentication.application.services import (
    AccountApplicationService,
    IdentityApplicationService,
    AuthApplicationService,
    ProviderApplicationService,
    SessionApplicationService,
)
from src.contexts.authentication.domain.entities import Identity, Provider
from src.contexts.authentication.domain.providers import IProvider, IProviderFactory
from src.contexts.authentication.domain.repositories import IAccountRepository, IIdentityRepository, IProviderRepository
from src.contexts.authentication.domain.value_objects import IdentityID, ProviderID, ProviderConfig, \
    ProviderPlainCredentials, ProviderSecureCredentials, ProviderName, ProviderType
from src.domain import IDatabaseContext
from src.domain.entities import Account
from src.domain.value_objects import AccountID


def create_mock_service_fixture(service_class: Type, **custom_mocks):
    @pytest.fixture
    def _mock_service(request):
        sig = inspect.signature(service_class.__init__)
        kwargs = {}

        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue

            if param_name in custom_mocks:
                kwargs[param_name] = custom_mocks[param_name]
            else:
                kwargs[param_name] = request.getfixturevalue(f'mock_{param_name}')

        return service_class(**kwargs)

    return _mock_service


account_service = create_mock_service_fixture(AccountApplicationService)
identity_service = create_mock_service_fixture(IdentityApplicationService)
auth_service = create_mock_service_fixture(AuthApplicationService)
provider_service = create_mock_service_fixture(ProviderApplicationService)
session_service = create_mock_service_fixture(SessionApplicationService)


@pytest.fixture
def mock_session_repository():
    from src.contexts.authentication.domain.repositories import ISessionRepository
    repo_mock = AsyncMock(spec=ISessionRepository)
    repo_mock.create.return_value = None
    repo_mock.get_by_id.return_value = None
    repo_mock.get_by_account_id.return_value = []
    repo_mock.get_by_account_and_provider.return_value = None
    repo_mock.update.return_value = None
    return repo_mock


@pytest.fixture
def mock_refresh_token_repository():
    from src.contexts.authentication.domain.repositories import IRefreshTokenRepository
    repo_mock = AsyncMock(spec=IRefreshTokenRepository)
    repo_mock.create.return_value = None
    repo_mock.get_by_id.return_value = None
    repo_mock.get_active_by_session.return_value = None
    repo_mock.update.return_value = None
    return repo_mock


@pytest.fixture
def mock_access_token_jwt_manager():
    from src.contexts.authentication.domain.value_objects import AuthContext
    manager_mock = AsyncMock()

    mock_context = MagicMock(spec=AuthContext)
    mock_context.identity_id = uuid.uuid4()
    mock_context.account_id = uuid.uuid4()

    manager_mock.validate = AsyncMock(return_value=mock_context)
    manager_mock.issue = AsyncMock(return_value=MagicMock(token="jwt_token"))
    return manager_mock


@pytest.fixture
def mock_provider_domain_service():
    from src.contexts.authentication.domain.services import ProviderService
    service_mock = AsyncMock(spec=ProviderService)
    service_mock.activate = MagicMock(return_value=(AsyncMock(), None))
    return service_mock


@pytest.fixture
def mock_domain_service(mock_provider_domain_service):
    """Alias for mock_provider_domain_service"""
    return mock_provider_domain_service


@pytest.fixture
def expected_id():
    return uuid.uuid4()


@pytest.fixture
def mock_account_repository(expected_id):
    repo_mock = AsyncMock(spec=IAccountRepository)
    repo_mock.create.return_value = None
    repo_mock.get_by_id.return_value = Account(id=AccountID(expected_id))
    return repo_mock


@pytest.fixture
def mock_identity(expected_id):
    return Identity(
        id=IdentityID(expected_id),
        account_id=AccountID(expected_id),
        provider_id=ProviderID(expected_id),
        credentials=dict(one=1),
        created_at=datetime.now(tz=timezone.utc),
        last_used_at=datetime.now(tz=timezone.utc)
    )


@pytest.fixture
def mock_identity_repository(mock_identity):
    repo_mock = AsyncMock(spec=IIdentityRepository)
    repo_mock.create.return_value = None
    repo_mock.get_by_id.return_value = mock_identity
    repo_mock.get_by_account_id.return_value = [mock_identity]
    repo_mock.get_by_account_and_provider.return_value = mock_identity
    repo_mock.get_by_provider_and_login.return_value = mock_identity
    repo_mock.update.return_value = None
    return repo_mock


@pytest.fixture
def mock_provider():
    provider = AsyncMock(spec=IProvider)
    provider.validate_config.return_value = ProviderConfig(
        access_token_expire_minutes=1,
        refresh_token_expire_days=1
    )
    provider.validate_credentials = AsyncMock(
        return_value=ProviderPlainCredentials()
    )
    provider.secure_credentials.return_value = ProviderSecureCredentials()
    provider.get_login_field.return_value = "test_user"
    provider.authenticate = AsyncMock(return_value=None)

    mock_access_token = MagicMock()
    mock_access_token.token = "access_token_value"
    provider.access_token_manager.issue = AsyncMock(return_value=mock_access_token)

    mock_refresh_token = MagicMock()
    mock_refresh_token.token = "refresh_token_value"
    provider.refresh_token_manager.issue = AsyncMock(return_value=mock_refresh_token)
    provider.refresh_token_manager.validate = AsyncMock(return_value=None)

    return provider


@pytest.fixture
def mock_provider_repository(mock_provider):
    repo_mock = AsyncMock(spec=IProviderRepository)
    provider_entity = Provider.create(
        name=ProviderName("provider_telegram"),
        type=ProviderType.TELEGRAM,
        config=dict(access_token_expire_minutes=1, refresh_token_expire_days=1)
    )
    repo_mock.create.return_value = None
    repo_mock.get_by_id.return_value = provider_entity
    repo_mock.get_by_type.return_value = [provider_entity]
    repo_mock.get_active_by_type.return_value = provider_entity
    repo_mock.update.return_value = None
    return repo_mock


@pytest.fixture
def mock_provider_registry(mock_provider):
    factory = MagicMock(spec=IProviderFactory)
    factory.get.return_value = mock_provider
    return factory


@pytest.fixture
def mock_database_context():
    ctx_mock = AsyncMock(spec=IDatabaseContext)
    ctx_mock.__aenter__.return_value = ctx_mock
    ctx_mock.__aexit__.return_value = True
    ctx_mock.connection = MagicMock()
    ctx_mock.use_transaction = AsyncMock(return_value=None)
    return ctx_mock


@pytest.fixture
def mock_session(mock_identity):
    """Mock Session entity"""
    from src.contexts.authentication.domain.entities import Session

    session = Session.create(mock_identity.account_id, mock_identity.provider_id)
    return session


@pytest.fixture
def mock_refresh_token(mock_session):
    """Mock RefreshToken entity - use MagicMock to avoid complex initialization"""
    from src.contexts.authentication.domain.entities import RefreshToken
    from src.contexts.authentication.domain.value_objects import RefreshTokenID

    refresh_token = MagicMock(spec=RefreshToken)
    refresh_token.id = RefreshTokenID(uuid.uuid4())
    refresh_token.session_id = mock_session.id
    refresh_token.hash = b"token_hash"
    refresh_token.revoke = MagicMock()
    refresh_token.is_active = MagicMock(return_value=True)
    return refresh_token
