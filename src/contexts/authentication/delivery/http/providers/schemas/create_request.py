from typing import Optional, Literal, Any

from pydantic import BaseModel, Field


class CreateProviderRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: Literal['telegram']
    config: Optional[dict[str, Any]] = None
