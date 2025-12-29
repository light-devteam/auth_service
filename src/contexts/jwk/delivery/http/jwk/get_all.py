from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from msgspec import structs

from src.contexts.jwk.delivery.http.jwk.router import router
from src.contexts.jwk.application import IJWKService
from src.contexts.jwk.delivery.http.jwk.schemas import JWKInfo


@router.get('')
@inject
async def get_all(
    page: int = 1,
    page_size: int = 100,
    only_active: bool = True,
    service: IJWKService = Depends(Provide['jwk_application_service']),
) -> list[JWKInfo]:
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 1
    jwk_tokens = await service.get_all(page, page_size, only_active)
    return [JWKInfo.model_validate(structs.asdict(jwk)) for jwk in jwk_tokens]
