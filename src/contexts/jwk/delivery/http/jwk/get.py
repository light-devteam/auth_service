from uuid import UUID

from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from msgspec import structs

from src.contexts.jwk.delivery.http.jwk.router import router
from src.contexts.jwk.application import JWKService
from src.contexts.jwk.delivery.http.jwk.schemas import JWKInfo


@router.get('/{jwk_id}')
@inject
async def get(
    jwk_id: UUID,
    service: JWKService = Depends(Provide['jwk_application_service']),
) -> JWKInfo:
    jwk = await service.get_by_id(jwk_id)
    return JWKInfo.model_validate(structs.asdict(jwk))
