from pydantic import BaseModel, Field


class CreateTokenRequestSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)
