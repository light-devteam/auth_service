from uuid import UUID

from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from src.jwk.delivery.http.jwk.router import router
from src.jwk.application import JWKService
from src.jwk.delivery.http.jwk.schemas import NewPrimaryJWK, JWKIsPrimary


@router.patch('/{jwk_id}/set_primary')
@inject
async def set_primary(
    jwk_id: UUID,
    service: JWKService = Depends(Provide['jwk_application_service']),
) -> NewPrimaryJWK:
    new, old = await service.set_primary(jwk_id)
    new_schema = JWKIsPrimary(id=new.id, is_primary=new.is_primary)
    old_schema = None
    if old:
        old_schema = JWKIsPrimary(id=old.id, is_primary=old.is_primary)
    return NewPrimaryJWK(new=new_schema, old=old_schema)
