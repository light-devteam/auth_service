from fastapi import Response, status

from fastapi import Depends

from src.contexts.authentication.delivery.http.auth.router import router
from src.delivery.dependencies import require_auth


@router.get('/introspect')
async def introspect(auth: str = Depends(require_auth)) -> Response:
    return Response(status_code=status.HTTP_200_OK)
