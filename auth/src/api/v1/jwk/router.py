from fastapi import APIRouter

router = APIRouter(
    prefix='/jwk',
    tags=['Json Web Keys'],
)
