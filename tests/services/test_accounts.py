import pytest

from src.domain.value_objects import AccountID
from tests.conftest import expected_id


@pytest.mark.asyncio
async def test_create_account(account_service, request):
    mock_repo = request.getfixturevalue('mock_account_repository')
    mock_ctx = request.getfixturevalue('mock_database_context')

    account = await account_service.create()

    assert account is not None
    assert account.id is not None

    mock_repo.create.assert_called_once_with(
        mock_ctx, account
    )
    mock_ctx.__aenter__.assert_called_once()
    mock_ctx.__aexit__.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id(account_service, expected_id, request):
    mock_repo = request.getfixturevalue('mock_account_repository')
    mock_ctx = request.getfixturevalue('mock_database_context')

    account = await account_service.get_by_id(expected_id)

    mock_repo.get_by_id.assert_called_once_with(
        mock_ctx, AccountID(expected_id)
    )
    assert account is not None
    assert account.id is not None
    assert account.id.__eq__(AccountID(expected_id))
