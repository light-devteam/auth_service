from src.contexts.jwk.domain.entities import JWKToken
from src.contexts.jwk.domain.exceptions import JWKAlreadyPrimary


class JWKTokenService:
    async def set_primary(
        self,
        new: JWKToken,
        old: JWKToken | None,
    ) -> tuple[JWKToken, JWKToken | None]:
        if new.is_primary:
            raise JWKAlreadyPrimary()
        new.activate()
        new.is_primary = not new.is_primary
        if old:
            old.is_primary = not old.is_primary
        return new, old
