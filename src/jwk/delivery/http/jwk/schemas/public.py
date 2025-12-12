from pydantic import BaseModel, ConfigDict

from src.domain.value_objects.enums import JWTAlgorithms


class JWKPublic(BaseModel):
    e: str
    n: str
    alg: JWTAlgorithms
    kid: str
    kty: str
    use: str

    model_config = ConfigDict(
        extra='allow',
    )
