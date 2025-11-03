from src.api.v1.jwk.router import router
from src.schemas import JWKInfoSchema
from src.services import JWKeysService
from package import json_encoder
from package import Token


@router.get('/')
async def get_all(
    page: int = 1,
    page_size: int = 100,
    only_active: bool = True,
) -> list[JWKInfoSchema]:
    get_keys = JWKeysService.get_keys
    if only_active:
        get_keys = JWKeysService.get_active_keys
    keys = await get_keys(page, page_size)
    return [JWKInfoSchema.model_validate_json(json_encoder.encode(key)) for key in keys]
