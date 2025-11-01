from uuid import UUID

from fastapi import Response, status

from src.api.v1.jwk.router import router
from src.services import JWKeysService


@router.post('/{key_id}/deactivate')
async def deactivate(key_id: UUID) -> None:
    await JWKeysService.deactivate_key(key_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
