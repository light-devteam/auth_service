from uuid import UUID

from src.api.v1.jwk.router import router
from src.schemas import JWKSchema
from src.services import JWKeysService
from package import json_encoder


@router.get('/{key_id}')
async def get(key_id: UUID) -> JWKSchema:
    key_data = await JWKeysService.get_key(key_id)
    key_data_json = json_encoder.encode(key_data)
    return JWKSchema.model_validate_json(key_data_json)
