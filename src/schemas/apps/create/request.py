from typing import Optional

from pydantic import BaseModel, Field

from src.enums import AppTypes


class CreateAppRequestSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    description: Optional[str] = Field('', max_length=255)
    type: AppTypes
