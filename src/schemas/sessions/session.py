from uuid import UUID

from pydantic import BaseModel

from src.schemas.sessions.token_pair import TokenPairSchema


class SessionSchema(BaseModel):
    session_id: UUID
    token_pair: TokenPairSchema
