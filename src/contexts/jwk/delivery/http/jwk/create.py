from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.jwk.delivery.http.jwk.router import router
from src.contexts.jwk.application import IJWKService
from src.contexts.jwk.delivery.http.jwk.schemas import CreateJWKRequest, CreateJWKResponse


@router.post('/create', status_code=status.HTTP_201_CREATED)
@inject
async def create(
    creation_data: CreateJWKRequest,
    service: IJWKService = Depends(Provide['jwk_application_service']),
) -> CreateJWKResponse:
    jwk = await service.create(creation_data.name)
    return CreateJWKResponse(id=jwk.id)
