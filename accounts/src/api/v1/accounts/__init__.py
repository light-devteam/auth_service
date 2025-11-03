from src.api.v1.accounts.router import router
from src.api.v1.accounts.get_all import router
from src.api.v1.accounts.get import router
from src.api.v1.accounts.get_by_telegram_id import router
from src.api.v1.accounts.create import router


__all__ = [
    'router',
]
