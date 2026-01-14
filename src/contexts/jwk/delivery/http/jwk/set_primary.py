from uuid import UUID

from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from src.contexts.jwk.delivery.http.jwk.router import router
from src.contexts.jwk.application import IJWKService
from src.contexts.jwk.delivery.http.jwk.schemas import NewPrimaryJWK, JWKIsPrimary
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.patch('/{jwk_id}/set_primary')
@inject
async def set_primary(
    jwk_id: UUID,
    service: IJWKService = Depends(Provide['jwk.service']),
    _: AuthContext = Depends(require_auth),
) -> NewPrimaryJWK:
    new, old = await service.set_primary(jwk_id)
    new_schema = JWKIsPrimary(id=new.id, is_primary=new.is_primary)
    old_schema = None
    if old:
        old_schema = JWKIsPrimary(id=old.id, is_primary=old.is_primary)
    return NewPrimaryJWK(new=new_schema, old=old_schema)
