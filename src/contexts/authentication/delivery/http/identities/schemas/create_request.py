from uuid import UUID
from typing import Any

from pydantic import BaseModel


class CreateIdentityRequest(BaseModel):
    account_id: UUID
    provider_id: UUID
    provider_data: dict[str, Any]
