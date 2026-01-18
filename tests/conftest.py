import inspect
import uuid
from datetime import timezone, datetime
from typing import Type
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.contexts.authentication.application.services import AccountApplicationService, IdentityApplicationService
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
    provider.validate_credentials.return_value = AsyncMock(
        return_value=ProviderPlainCredentials()
    )
    provider.secure_credentials.return_value = ProviderSecureCredentials()
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
