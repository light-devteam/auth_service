from typing import Optional

from pydantic import BaseModel

from src.contexts.authentication.delivery.http.providers.schemas.active_state import ActiveState


class ActivateResponse(BaseModel):
    new: ActiveState
    old: Optional[ActiveState]
