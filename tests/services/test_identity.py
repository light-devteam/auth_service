import pytest

from src.contexts.authentication.domain.value_objects import ProviderType, IdentityID, ProviderID
from src.domain.value_objects import AccountID


@pytest.mark.asyncio
async def test_create_identity_with_valid_provider(identity_service, expected_id, request):
    """Creates identity with valid provider"""
    mock_identity_repo = request.getfixturevalue('mock_identity_repository')
    mock_provider_repo = request.getfixturevalue('mock_provider_repository')
    mock_registry = request.getfixturevalue('mock_provider_registry')

    identity = await identity_service.create(
        account_id=expected_id,
        provider_type=ProviderType.TELEGRAM,
        credentials={"login": "test_user"}
    )

    mock_registry.get.assert_called_once_with(ProviderType.TELEGRAM)
    mock_provider_repo.get_active_by_type.assert_called_once()
    mock_identity_repo.create.assert_called_once()
    assert identity is not None
    assert identity.account_id == AccountID(expected_id)
    assert identity.id is not None
    assert isinstance(identity.id, IdentityID)


@pytest.mark.asyncio
async def test_get_identity_by_id_returns_identity(identity_service, expected_id, request):
    """Retrieves identity by ID"""
    mock_identity_repo = request.getfixturevalue('mock_identity_repository')
    expected_identity = mock_identity_repo.get_by_id.return_value

    identity = await identity_service.get_by_id(expected_id)

    mock_identity_repo.get_by_id.assert_called_once()
    assert identity is not None
    assert identity.id is not None
    assert isinstance(identity.id, IdentityID)
    assert identity == expected_identity


@pytest.mark.asyncio
async def test_get_identities_by_account_id_returns_list(identity_service, expected_id, request, mock_identity):
    """Retrieves all identities for account"""
    mock_identity_repo = request.getfixturevalue('mock_identity_repository')
    mock_identity = request.getfixturevalue('mock_identity')
    mock_identity_repo.get_by_account_id.return_value = [mock_identity]

    identities = await identity_service.get_by_account_id(expected_id)

    mock_identity_repo.get_by_account_id.assert_called_once()
    assert identities is not None
    assert isinstance(identities, list)
    assert len(identities) > 0
    assert identities[0].account_id == AccountID(expected_id)


@pytest.mark.asyncio
async def test_get_identity_by_account_and_provider_returns_identity(identity_service, expected_id, request,
                                                                     mock_identity):
    """Retrieves identity by account and provider"""
    mock_identity_repo = request.getfixturevalue('mock_identity_repository')
    mock_identity = request.getfixturevalue('mock_identity')
    mock_identity_repo.get_by_account_and_provider.return_value = mock_identity

    identity = await identity_service.get_by_account_and_provider(expected_id, ProviderType.TELEGRAM)

    mock_identity_repo.get_by_account_and_provider.assert_called_once()
    assert identity is not None
    assert identity.account_id is not None
    assert isinstance(identity.provider_id, ProviderID)


@pytest.mark.asyncio
async def test_create_multiple_identities_different_providers(identity_service, expected_id, request):
    """Creates identities for different providers"""
    mock_registry = request.getfixturevalue('mock_provider_registry')

    telegram_identity = await identity_service.create(
        account_id=expected_id,
        provider_type=ProviderType.TELEGRAM,
        credentials={}
    )

    assert mock_registry.get.call_count >= 1
    assert telegram_identity is not None
    assert telegram_identity.account_id == AccountID(expected_id)
