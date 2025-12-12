from uuid import UUID

from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from src.jwk.delivery.http.jwk.router import router
from src.jwk.application import JWKService
from src.jwk.delivery.http.jwk.schemas import JWKIsActive


@router.patch('/{jwk_id}/toggle_active')
@inject
async def toggle_active(
    jwk_id: UUID,
    service: JWKService = Depends(Provide['jwk_application_service']),
) -> JWKIsActive:
    jwk = await service.toggle_active(jwk_id)
    return JWKIsActive(id=jwk_id, is_active=jwk.is_active)
