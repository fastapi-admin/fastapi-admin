from typing import Dict, List, Optional, Type

from aioredis import Redis
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from tortoise import Model

from fastapi_admin import i18n
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
)

from . import middlewares, template
from .providers import Provider
from .resources import Dropdown
from .resources import Model as ModelResource
from .resources import Resource
from .routes import router


class FastAPIAdmin(FastAPI):
    logo_url: str
    login_logo_url: str
    admin_path: str
    resources: List[Type[Resource]] = []
    model_resources: Dict[Type[Model], Type[Resource]] = {}
    redis: Redis

    async def configure(
        self,
        redis: Redis,
        logo_url: str = None,
        login_logo_url: str = None,
        default_locale: str = "en_US",
        admin_path: str = "/admin",
        template_folders: Optional[List[str]] = None,
        providers: Optional[List[Provider]] = None,
    ):
        self.redis = redis
        self.login_logo_url = login_logo_url
        i18n.set_locale(default_locale)
        self.admin_path = admin_path
        self.logo_url = logo_url
        if template_folders:
            template.add_template_folder(*template_folders)
        await self._register_providers(providers)

    async def _register_providers(self, providers: Optional[List[Provider]] = None):
        for p in providers or []:
            await p.register(self)

    def register_resources(self, *resource: Type[Resource]):
        for r in resource:
            self.register(r)

    def _set_model_resource(self, resource: Type[Resource]):
        if issubclass(resource, ModelResource):
            self.model_resources[resource.model] = resource
        elif issubclass(resource, Dropdown):
            for r in resource.resources:
                self._set_model_resource(r)

    def register(self, resource: Type[Resource]):
        self._set_model_resource(resource)
        self.resources.append(resource)

    def get_model_resource(self, model: Type[Model]):
        return self.model_resources[model]()


app = FastAPIAdmin(
    title="FastAdmin",
    description="A fast admin dashboard based on fastapi and tortoise-orm with tabler ui.",
)
app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.language_processor)
app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
app.include_router(router)
