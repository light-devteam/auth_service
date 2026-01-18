import pytest

from src.domain.value_objects import AccountID


@pytest.mark.asyncio
async def test_create_account(account_service, request):
    """Creates account with unique ID"""
    mock_repo = request.getfixturevalue('mock_account_repository')

    account = await account_service.create()

    assert account is not None
    assert account.id is not None
    mock_repo.create.assert_called_once()
    call_args = mock_repo.create.call_args
    assert call_args[0][1] == account


@pytest.mark.asyncio
async def test_get_account_by_id_returns_account(account_service, expected_id, request):
    """Retrieves account by ID"""
    mock_repo = request.getfixturevalue('mock_account_repository')
    expected_account = mock_repo.get_by_id.return_value

    account = await account_service.get_by_id(expected_id)

    mock_repo.get_by_id.assert_called_once()
    call_args = mock_repo.get_by_id.call_args[0]
    assert AccountID(expected_id) == call_args[1]
    assert account is not None
    assert account.id is not None
    assert account.id == expected_account.id


@pytest.mark.asyncio
async def test_create_account_idempotent(account_service):
    """Each created account has unique ID"""
    account1 = await account_service.create()
    account2 = await account_service.create()
    
    assert account1.id != account2.id
