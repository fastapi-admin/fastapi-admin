from typing import Dict, List, Optional, Type

from aioredis import Redis
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise import Model

from fastapi_admin import i18n

from . import middlewares, template
from .providers.login import LoginProvider
from .resources import Dropdown
from .resources import Model as ModelResource
from .resources import Resource
from .routes import router


class FastAdmin(FastAPI):
    logo_url: str
    login_logo_url: str
    admin_path: str
    resources: List[Type[Resource]] = []
    model_resources: Dict[Type[Model], Type[Resource]] = {}
    login_provider: Optional[LoginProvider]
    redis: Redis

    def configure(
        self,
        redis: Redis,
        logo_url: str = None,
        login_logo_url: str = None,
        default_locale: str = "en_US",
        admin_path: str = "/admin",
        template_folders: Optional[List[str]] = None,
        login_provider: Optional[LoginProvider] = None,
    ):
        """
        Config FastAdmin
        :param logo_url:
        :param default_locale:
        :param admin_path:
        :param template_folders:
        :param login_provider:
        :return:
        """
        self.redis = redis
        self.login_logo_url = login_logo_url
        i18n.set_locale(default_locale)
        self.admin_path = admin_path
        self.logo_url = logo_url
        if template_folders:
            template.add_template_folder(*template_folders)
        self.login_provider = login_provider
        self._register_providers()

    def _register_providers(self):
        if self.login_provider:
            login_path = self.login_provider.login_path
            app.get(login_path)(self.login_provider.get)
            app.post(login_path)(self.login_provider.post)
            app.get(self.login_provider.logout_path)(self.login_provider.logout)
            app.add_middleware(BaseHTTPMiddleware, dispatch=self.login_provider.authenticate)

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


app = FastAdmin(
    title="FastAdmin",
    description="A fast admin dashboard based on fastapi and tortoise-orm with tabler ui.",
)
app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.language_processor)
app.include_router(router)
