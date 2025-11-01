from pydantic import BaseModel


class JWKSSchema(BaseModel):
    keys: list[dict]
