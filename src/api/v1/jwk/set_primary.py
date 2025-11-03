from uuid import UUID

from fastapi import Response, status

from src.api.v1.jwk.router import router
from src.services import JWKeysService


@router.post('{key_id}/set_primary')
async def set_primary(key_id: UUID) -> None:
    await JWKeysService.set_primary(key_id)
    await JWKeysService.set_private_key_to_config()
    await JWKeysService.set_jwks_to_config()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
