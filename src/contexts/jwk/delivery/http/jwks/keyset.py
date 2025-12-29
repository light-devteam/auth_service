from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from src.contexts.jwk.delivery.http.jwks.router import router
from src.contexts.jwk.delivery.http.jwks.schemas import JWKS
from src.contexts.jwk.application.interfaces import IJWKService


@router.get('/jwks.json')
@inject
async def jwks(
    page: int = 1,
    page_size: int = 100,
    service: IJWKService = Depends(Provide['jwk_application_service']),
) -> JWKS:
    jwk_tokens = await service.get_all(page, page_size, only_active=True)
    keyset = []
    for jwk in jwk_tokens:
        keyset.append(jwk.public)
    return JWKS(keys=keyset)
