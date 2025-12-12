from pydantic import BaseModel, Field


class CreateJWKRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
