from typing import Awaitable, Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class IPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Awaitable) -> Any:
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        x_real_ip = request.headers.get('X-Real-IP')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        elif x_real_ip:
            ip = x_real_ip
        else:
            ip = request.client.host
        request.state.ip = ip
        response = await call_next(request)
        return response
