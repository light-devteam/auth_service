from typing import Optional

from pydantic import BaseModel

from src.contexts.jwk.delivery.http.jwk.schemas.is_primary import JWKIsPrimary


class NewPrimaryJWK(BaseModel):
    new: JWKIsPrimary
    old: Optional[JWKIsPrimary]
