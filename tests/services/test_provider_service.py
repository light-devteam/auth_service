import pytest
from unittest.mock import MagicMock

from src.contexts.authentication.domain.services.provider import ProviderService
from src.contexts.authentication.domain.exceptions import ProviderAlreadyActive


@pytest.fixture
def provider_domain_service():
    """Provider domain service instance"""
    return ProviderService()


@pytest.fixture
def mock_provider_entity():
    """Mock Provider entity"""
    provider = MagicMock()
    provider.is_active = False
    provider.activate = MagicMock()
    return provider


@pytest.fixture
def mock_old_provider():
    """Mock old Provider entity"""
    provider = MagicMock()
    provider.is_active = True
    return provider


@pytest.mark.asyncio
async def test_activate_provider_with_no_old(provider_domain_service, mock_provider_entity):
    """Activates new provider when no old provider exists"""
    new, old = provider_domain_service.activate(mock_provider_entity, None)

    assert new == mock_provider_entity
    assert old is None
    mock_provider_entity.activate.assert_called_once()


@pytest.mark.asyncio
async def test_activate_provider_replaces_old(provider_domain_service, mock_provider_entity, mock_old_provider):
    """Deactivates old provider when activating new one"""
    new, old = provider_domain_service.activate(mock_provider_entity, mock_old_provider)

    assert new == mock_provider_entity
    assert old == mock_old_provider
    mock_provider_entity.activate.assert_called_once()
    assert old.is_active is False


@pytest.mark.asyncio
async def test_activate_raises_when_provider_already_active(provider_domain_service, mock_provider_entity):
    """Raises error when trying to activate already active provider"""
    mock_provider_entity.is_active = True

    with pytest.raises(ProviderAlreadyActive):
        provider_domain_service.activate(mock_provider_entity, None)

    mock_provider_entity.activate.assert_not_called()


@pytest.mark.asyncio
async def test_activate_returns_both_providers(provider_domain_service, mock_provider_entity, mock_old_provider):
    """Returns tuple of new and old providers"""
    result = provider_domain_service.activate(mock_provider_entity, mock_old_provider)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == mock_provider_entity
    assert result[1] == mock_old_provider
