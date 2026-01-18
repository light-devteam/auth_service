import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.contexts.authentication.domain.repositories import IAccountRepository
from src.domain import IDatabaseContext
from src.domain.entities import Account
from src.domain.value_objects import AccountID

@pytest.fixture
def expected_id():
    return uuid.uuid4()

@pytest.fixture
def mock_account_repository():
    repo_mock = AsyncMock(spec=IAccountRepository)
    repo_mock.create.return_value = None
    repo_mock.get_by_id.return_value = Account(id=AccountID())
    return repo_mock


@pytest.fixture
def mock_database_context():
    ctx_mock = AsyncMock(spec=IDatabaseContext)
    ctx_mock.__aenter__.return_value = ctx_mock
    ctx_mock.__aexit__.return_value = True
    ctx_mock.connection = MagicMock()
    return ctx_mock
