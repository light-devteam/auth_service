from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.contexts.authentication.domain import value_objects, exceptions


@pytest.mark.asyncio
async def test_introspect_empty_token(request):
    """Rejects empty token"""
    auth_service = request.getfixturevalue('auth_service')

    with pytest.raises(exceptions.InvalidToken, match="Access token invalid"):
        await auth_service.introspect("")


@pytest.mark.asyncio
async def test_introspect_opaque_token_rejected(request):
    """Rejects opaque token format"""
    auth_service = request.getfixturevalue('auth_service')
    token = "token_id:token_value"

    with pytest.raises(exceptions.InvalidToken, match="Access token invalid"):
        await auth_service.introspect(token)


@pytest.mark.asyncio
async def test_introspect_valid_jwt_token(request):
    """Validates JWT token successfully"""
    auth_service = request.getfixturevalue('auth_service')
    mock_jwt_manager = request.getfixturevalue('mock_access_token_jwt_manager')

    mock_context = MagicMock(spec=value_objects.AuthContext)
    mock_context.identity_id = uuid4()
    mock_context.account_id = uuid4()
    mock_jwt_manager.validate = AsyncMock(return_value=mock_context)

    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.signature"
    result = await auth_service.introspect(jwt_token)

    assert result == mock_context
    assert mock_jwt_manager.validate.called


@pytest.mark.asyncio
async def test_refresh_invalid_token_format(request):
    """Rejects invalid token format"""
    auth_service = request.getfixturevalue('auth_service')

    with pytest.raises((ValueError, exceptions.InvalidToken)):
        await auth_service.refresh("invalid_token_no_colon")


@pytest.mark.asyncio
async def test_get_token_type_jwt(request):
    """Identifies JWT tokens"""
    auth_service = request.getfixturevalue('auth_service')

    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.payload.signature"
    token_type = auth_service._AuthApplicationService__get_token_type(jwt_token)

    assert token_type == "jwt"


@pytest.mark.asyncio
async def test_get_token_type_opaque(request):
    """Identifies opaque tokens"""
    auth_service = request.getfixturevalue('auth_service')

    opaque_token = "token_id:token_value"
    token_type = auth_service._AuthApplicationService__get_token_type(opaque_token)

    assert token_type == "opaque"


@pytest.mark.asyncio
async def test_get_token_success(request, mock_provider, mock_provider_registry):
    """Generates tokens successfully"""
    auth_service = request.getfixturevalue('auth_service')
    mock_provider_registry = request.getfixturevalue('mock_provider_registry')
    request.getfixturevalue('mock_provider_repository')
    request.getfixturevalue('mock_identity_repository')
    request.getfixturevalue('mock_session_repository')
    request.getfixturevalue('mock_refresh_token_repository')
    request.getfixturevalue('mock_identity')

    mock_provider = mock_provider_registry.get.return_value

    access_token, refresh_token = await auth_service.get_token(
        value_objects.ProviderType.TELEGRAM,
        {"login": "test_user"}
    )

    assert access_token is not None
    assert refresh_token is not None
    mock_provider.validate_config.assert_called()
    mock_provider.validate_credentials.assert_called()
    mock_provider.authenticate.assert_called()


@pytest.mark.asyncio
async def test_refresh_token_success(request, mock_refresh_token, mock_session, mock_provider_registry, mock_provider):
    """Refreshes token successfully"""
    auth_service = request.getfixturevalue('auth_service')
    mock_provider_registry = request.getfixturevalue('mock_provider_registry')
    request.getfixturevalue('mock_provider_repository')
    request.getfixturevalue('mock_identity_repository')
    mock_session_repo = request.getfixturevalue('mock_session_repository')
    mock_refresh_token_repo = request.getfixturevalue('mock_refresh_token_repository')
    request.getfixturevalue('mock_identity')
    mock_session = request.getfixturevalue('mock_session')
    mock_refresh_token = request.getfixturevalue('mock_refresh_token')

    mock_refresh_token_repo.get_by_id.return_value = mock_refresh_token
    mock_session_repo.get_by_id.return_value = mock_session

    mock_provider = mock_provider_registry.get.return_value

    token_string = f"{mock_refresh_token.id}:refresh_token_value"
    access_token, refresh_token = await auth_service.refresh(token_string)

    assert access_token is not None
    assert refresh_token is not None
    mock_provider.refresh_token_manager.validate.assert_called_once()
    mock_refresh_token_repo.get_by_id.assert_called_once()
    mock_session_repo.get_by_id.assert_called_once()
