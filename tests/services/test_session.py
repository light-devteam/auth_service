from unittest.mock import MagicMock

import pytest

from src.contexts.authentication.domain import value_objects
from src.domain.value_objects import AccountID


@pytest.mark.asyncio
async def test_create_session_with_valid_provider(request):
    """Test creating a session with valid provider"""
    session_service = request.getfixturevalue('session_service')
    mock_provider_repo = request.getfixturevalue('mock_provider_repository')

    account_id = request.getfixturevalue('expected_id')

    mock_provider = MagicMock()
    mock_provider.id = account_id
    mock_provider_repo.get_active_by_type.return_value = mock_provider

    session = await session_service.create(account_id, value_objects.ProviderType.TELEGRAM)

    assert session is not None
    assert session.id is not None
    assert session.account_id == AccountID(account_id)
    assert session.is_active() is True


@pytest.mark.asyncio
async def test_get_session_by_id(request, mock_identity):
    """Test getting session by ID from repository"""
    session_service = request.getfixturevalue('session_service')
    mock_session_repo = request.getfixturevalue('mock_session_repository')

    session_id = request.getfixturevalue('expected_id')
    mock_identity = request.getfixturevalue('mock_identity')

    from src.contexts.authentication.domain.entities import Session
    test_session = Session.create(AccountID(session_id), mock_identity.provider_id)
    mock_session_repo.get_by_id.return_value = test_session

    session = await session_service.get_by_id(session_id)

    assert session is not None
    assert session.id is not None
    assert session.account_id == AccountID(session_id)
    mock_session_repo.get_by_id.assert_called_once()


@pytest.mark.asyncio
async def test_get_sessions_by_account_id(request):
    """Test getting all sessions for an account"""
    session_service = request.getfixturevalue('session_service')
    mock_session_repo = request.getfixturevalue('mock_session_repository')
    account_id = request.getfixturevalue('expected_id')

    mock_sessions = [
        MagicMock(id="session_1", account_id=AccountID(account_id), is_active=lambda: True),
        MagicMock(id="session_2", account_id=AccountID(account_id), is_active=lambda: True),
    ]
    mock_session_repo.get_by_account_id.return_value = mock_sessions

    sessions = await session_service.get_by_account_id(account_id)

    assert sessions is not None
    assert len(sessions) == 2
    mock_session_repo.get_by_account_id.assert_called_once()


@pytest.mark.asyncio
async def test_get_session_by_account_and_provider(request, mock_identity):
    """Test getting session by account and provider combination"""
    session_service = request.getfixturevalue('session_service')
    mock_session_repo = request.getfixturevalue('mock_session_repository')
    mock_identity = request.getfixturevalue('mock_identity')
    account_id = request.getfixturevalue('expected_id')

    from src.contexts.authentication.domain.entities import Session
    test_session = Session.create(AccountID(account_id), mock_identity.provider_id)
    mock_session_repo.get_by_account_and_provider.return_value = test_session

    session = await session_service.get_by_account_and_provider(account_id, value_objects.ProviderType.TELEGRAM)

    assert session is not None
    assert session.account_id == AccountID(account_id)
    mock_session_repo.get_by_account_and_provider.assert_called_once()


@pytest.mark.asyncio
async def test_revoke_session(request):
    """Test revoking an active session"""
    session_service = request.getfixturevalue('session_service')
    mock_session_repo = request.getfixturevalue('mock_session_repository')
    mock_refresh_token_repo = request.getfixturevalue('mock_refresh_token_repository')
    session_id = request.getfixturevalue('expected_id')

    from src.contexts.authentication.domain.entities import Session
    from src.contexts.authentication.domain.value_objects import ProviderID

    test_session = Session.create(AccountID(session_id), ProviderID(session_id))

    mock_refresh_token = MagicMock()
    mock_refresh_token.session_id = test_session.id
    mock_refresh_token.revoke = MagicMock()

    mock_session_repo.get_by_id.return_value = test_session
    mock_refresh_token_repo.get_active_by_session.return_value = mock_refresh_token

    await session_service.revoke(session_id)

    assert mock_session_repo.get_by_id.called
    assert mock_refresh_token.revoke.called
