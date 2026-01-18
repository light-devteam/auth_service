import pytest

from src.contexts.authentication.domain.value_objects import ProviderType, IdentityID
from src.domain.value_objects import AccountID


@pytest.mark.asyncio
async def test_identity_create(identity_service, expected_id, request):
    mock_identity_repo = request.getfixturevalue('mock_identity_repository')
    mock_provider_repo = request.getfixturevalue('mock_provider_repository')
    mock_registry = request.getfixturevalue('mock_provider_registry')
    mock_db_ctx = request.getfixturevalue('mock_database_context')

    identity = await identity_service.create(
        account_id=expected_id,
        provider_type=ProviderType.TELEGRAM,
        credentials=dict()
    )

    mock_registry.get.assert_called_once_with(ProviderType.TELEGRAM)
    mock_provider_repo.get_active_by_type.assert_called_once()
    mock_identity_repo.create.assert_called_once()
    mock_db_ctx.use_transaction.assert_called_once()

    assert identity is not None
    assert identity.account_id is not None
    assert identity.account_id.__eq__(AccountID(expected_id))
    assert identity.id is not None


@pytest.mark.asyncio
async def test_get_by_id(identity_service, expected_id, request):
    mock_identity_repo = request.getfixturevalue('mock_identity_repository')

    identity = await identity_service.get_by_id(expected_id)

    mock_identity_repo.get_by_id.assert_called_once()

    assert identity is not None
    assert identity.id is not None
    assert identity.id.__eq__(IdentityID(expected_id))


@pytest.mark.asyncio
async def test_get_by_account_id(identity_service, expected_id, request):
    mock_identity_repo = request.getfixturevalue('mock_identity_repository')

    identity = (await identity_service.get_by_account_id(expected_id))[0]

    mock_identity_repo.get_by_account_id.assert_called_once()

    assert identity is not None
    assert identity.account_id is not None
    assert identity.account_id.__eq__(expected_id)


@pytest.mark.asyncio
async def test_get_by_account_and_provider(identity_service, expected_id, request):
    mock_identity_repo = request.getfixturevalue('mock_identity_repository')

    identity = await identity_service.get_by_account_and_provider(expected_id, ProviderType.TELEGRAM)

    mock_identity_repo.get_by_account_and_provider.assert_called_once()

    assert identity is not None
    assert identity.provider_id is not None
    assert identity.provider_id.__eq__(expected_id)

# TODO УБРАТЬ expected_id И ЗАМЕНИТЬ на account_id, identity_id, etc.