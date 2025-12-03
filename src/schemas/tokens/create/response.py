from pydantic import BaseModel


class CreateTokenResponseSchema(BaseModel):
    token: str
