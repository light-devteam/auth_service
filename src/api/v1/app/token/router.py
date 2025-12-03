from fastapi import APIRouter


router = APIRouter(
    prefix='/{app_id}/token',
    tags=['Tokens']
)
