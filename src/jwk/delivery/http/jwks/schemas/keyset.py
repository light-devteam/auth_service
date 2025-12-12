from pydantic import BaseModel

from src.jwk.delivery.http.jwk.schemas import JWKPublic


class JWKS(BaseModel):
    keys: list[JWKPublic]