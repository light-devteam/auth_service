from typing import Optional, Any

from pydantic import BaseModel, Field


class CreateProviderRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    config: Optional[dict[str, Any]] = None
