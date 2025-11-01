from uuid import UUID

from fastapi import Response, status

from src.api.v1.jwk.router import router
from src.services import JWKeysService


@router.post('/{key_id}/activate')
async def activate(key_id: UUID) -> None:
    await JWKeysService.activate_key(key_id)
    await JWKeysService.set_jwks_to_config()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
