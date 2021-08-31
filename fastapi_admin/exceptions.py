from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from fastapi_admin.template import templates


class ServerHTTPException(HTTPException):
    def __init__(self, error: str = None):
        super(ServerHTTPException, self).__init__(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error
        )


class InvalidResource(ServerHTTPException):
    """
    raise when has invalid resource
    """


class NoSuchFieldFound(ServerHTTPException):
    """
    raise when no such field for the given
    """


class FileMaxSizeLimit(ServerHTTPException):
    """
    raise when the upload file exceeds the max size
    """


class FileExtNotAllowed(ServerHTTPException):
    """
    raise when the upload file ext not allowed
    """


async def server_error_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/500.html",
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        context={"request": request},
    )


async def not_found_error_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/404.html", status_code=exc.status_code, context={"request": request}
    )


async def forbidden_error_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/403.html", status_code=exc.status_code, context={"request": request}
    )


async def unauthorized_error_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/401.html", status_code=exc.status_code, context={"request": request}
    )
