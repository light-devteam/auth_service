from pydantic import BaseModel

from src.contexts.jwk.delivery.http.jwk.schemas import JWKPublic


class JWKS(BaseModel):
    keys: list[JWKPublic]