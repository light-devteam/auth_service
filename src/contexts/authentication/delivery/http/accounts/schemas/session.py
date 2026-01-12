from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Session(BaseModel):
    id: UUID
    account_id: UUID
    provider_id: UUID
    created_at: datetime
    revoked_at: Optional[datetime] = None
