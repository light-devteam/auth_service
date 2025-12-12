from uuid import UUID

from pydantic import BaseModel


class JWKIsPrimary(BaseModel):
    id: UUID
    is_primary: bool
