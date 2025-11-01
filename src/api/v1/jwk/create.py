from src.api.v1.jwk.router import router
from src.schemas import RequestCreateJWKSchema, ResponseCreateJWKSchema
from src.services import JWKeysService


@router.post('/create')
async def create(creation_data: RequestCreateJWKSchema) -> ResponseCreateJWKSchema:
    key_id = await JWKeysService.create_key(creation_data.name)
    return ResponseCreateJWKSchema(id=key_id)
