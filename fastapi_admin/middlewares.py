from typing import Callable

from starlette.requests import Request

from fastapi_admin import i18n


async def language_processor(request: Request, call_next: Callable):
    locale = request.query_params.get("language")
    if not locale:
        locale = request.cookies.get("language")
        if not locale:
            accept_language = request.headers.get("Accept-Language")
            if accept_language:
                locale = accept_language.split(",")[0].replace("-", "_")
            else:
                locale = None
    i18n.set_locale(locale)
    response = await call_next(request)
    if locale:
        response.set_cookie(key="language", value=locale)
    return response
