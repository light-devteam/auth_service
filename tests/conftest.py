from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_account_repository():
    ctx_mock = AsyncMock()
    repo = AsyncMock(spec=)