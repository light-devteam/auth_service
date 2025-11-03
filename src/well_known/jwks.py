from src.well_known.router import router
from src.schemas import JWKSSchema
from src.services import JWKeysService


@router.get('/jwks.json')
async def jwks(page: int = 1, page_size: int = 100) -> JWKSSchema:
    jwks_dto = await JWKeysService.get_jwks(page, page_size)
    return JWKSSchema(keys=jwks_dto.keys)
