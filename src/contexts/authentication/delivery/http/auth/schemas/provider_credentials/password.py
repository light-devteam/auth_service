from pydantic import BaseModel, Field


class PasswordProviderCredentials(BaseModel):
    login: str = Field(min_length=4, max_length=255)
    password: str = Field(min_length=6, max_length=72)
