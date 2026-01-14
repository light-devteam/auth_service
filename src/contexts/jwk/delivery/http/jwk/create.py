from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.jwk.delivery.http.jwk.router import router
from src.contexts.jwk.application import IJWKService
from src.contexts.jwk.delivery.http.jwk.schemas import CreateJWKRequest, CreateJWKResponse
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.post('/create', status_code=status.HTTP_201_CREATED)
@inject
async def create(
    creation_data: CreateJWKRequest,
    service: IJWKService = Depends(Provide['jwk.service']),
    _: AuthContext = Depends(require_auth),
) -> CreateJWKResponse:
    jwk = await service.create(creation_data.name)
    return CreateJWKResponse(id=jwk.id)
