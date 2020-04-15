from starlette.requests import Request
from fastapi.exceptions import HTTPException
from starlette.responses import UJSONResponse


async def exception_handler(request: Request, exc: HTTPException):
    return UJSONResponse(
        status_code=exc.status_code,
        content={'message': exc.detail},
    )
