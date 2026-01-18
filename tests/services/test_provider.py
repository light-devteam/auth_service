from unittest.mock import MagicMock

import pytest

from src.contexts.authentication.domain import value_objects


@pytest.mark.asyncio
async def test_create_provider(request, mock_provider_registry, mock_provider):
    """Test creating a provider with valid config"""
    provider_service = request.getfixturevalue('provider_service')
    mock_provider_registry = request.getfixturevalue('mock_provider_registry')

    mock_provider = mock_provider_registry.get.return_value
    mock_provider.validate_config.return_value = {"key": "value"}

    config = {"access_token_expire_minutes": 60, "refresh_token_expire_days": 30}
    provider = await provider_service.create("telegram_oauth", "telegram", config)

    assert provider is not None
    assert str(provider.name) == "telegram_oauth"
    assert provider.type == value_objects.ProviderType.TELEGRAM
    mock_provider.validate_config.assert_called_once()


@pytest.mark.asyncio
async def test_get_provider_types(request):
    """Test getting all available provider types"""
    provider_service = request.getfixturevalue('provider_service')

    types = await provider_service.get_types()

    assert types is not None
    assert len(types) > 0
    assert value_objects.ProviderType.TELEGRAM.value in types
    for provider_type in value_objects.ProviderType:
        assert provider_type.value in types


@pytest.mark.asyncio
async def test_get_provider_by_id(request):
    """Test getting provider by ID from repository"""
    provider_service = request.getfixturevalue('provider_service')
    mock_provider_repo = request.getfixturevalue('mock_provider_repository')
    provider_id = request.getfixturevalue('expected_id')

    mock_provider_entity = MagicMock()
    mock_provider_entity.id = provider_id
    mock_provider_entity.name = "test_provider"
    mock_provider_repo.get_by_id.return_value = mock_provider_entity

    provider = await provider_service.get_by_id(provider_id)

    assert provider is not None
    assert provider.id == provider_id
    mock_provider_repo.get_by_id.assert_called_once()


@pytest.mark.asyncio
async def test_get_provider_by_type(request):
    """Test getting providers by specific type"""
    provider_service = request.getfixturevalue('provider_service')
    mock_provider_repo = request.getfixturevalue('mock_provider_repository')

    mock_providers = [MagicMock(type=value_objects.ProviderType.TELEGRAM)]
    mock_provider_repo.get_by_type.return_value = mock_providers

    providers = await provider_service.get_by_type(value_objects.ProviderType.TELEGRAM.value)

    assert providers is not None
    assert len(providers) > 0
    mock_provider_repo.get_by_type.assert_called_once()


@pytest.mark.asyncio
async def test_get_active_provider_by_type(request):
    """Test getting active provider by type"""
    provider_service = request.getfixturevalue('provider_service')
    mock_provider_repo = request.getfixturevalue('mock_provider_repository')

    mock_active_provider = MagicMock()
    mock_active_provider.is_active = True
    mock_active_provider.type = value_objects.ProviderType.TELEGRAM
    mock_provider_repo.get_active_by_type.return_value = mock_active_provider

    provider = await provider_service.get_active_by_type(value_objects.ProviderType.TELEGRAM.value)

    assert provider is not None
    assert provider.is_active is True
    mock_provider_repo.get_active_by_type.assert_called_once()


@pytest.mark.asyncio
async def test_activate_provider(request):
    """Test activating a provider"""
    provider_service = request.getfixturevalue('provider_service')
    mock_provider_repo = request.getfixturevalue('mock_provider_repository')
    provider_id = request.getfixturevalue('expected_id')

    mock_provider = MagicMock()
    mock_provider.id = provider_id
    mock_provider.is_active = False
    mock_provider_repo.get_by_id.return_value = mock_provider

    result = await provider_service.activate(provider_id)

    assert result is not None
    mock_provider_repo.get_by_id.assert_called_once()
