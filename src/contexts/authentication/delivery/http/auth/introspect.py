from fastapi import Response, status

from src.contexts.authentication.delivery.http.auth.router import router


@router.get('/introspect')
async def introspect() -> Response:
    return Response(status_code=status.HTTP_200_OK)
