from fastapi import Response, status

from fastapi import Depends

from src.contexts.authentication.delivery.http.auth.router import router
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.get('/introspect')
async def introspect(_: AuthContext = Depends(require_auth)) -> Response:
    return Response(status_code=status.HTTP_200_OK)
