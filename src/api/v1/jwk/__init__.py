from src.api.v1.jwk.router import router
from src.api.v1.jwk.create import router
from src.api.v1.jwk.get import router
from src.api.v1.jwk.activate import router
from src.api.v1.jwk.deactivate import router
from src.api.v1.jwk.get_all import router

__all__ = [
    'router'
]
