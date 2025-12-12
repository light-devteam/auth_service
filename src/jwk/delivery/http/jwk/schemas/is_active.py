from uuid import UUID

from pydantic import BaseModel


class JWKIsActive(BaseModel):
    id: UUID
    is_active: bool
