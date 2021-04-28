import uuid
from gettext import gettext as _
from typing import Callable, Type

import bcrypt
from aioredis import Redis
from fastapi import Depends
from pydantic import EmailStr
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_401_UNAUTHORIZED
from tortoise import Model, fields

from fastapi_admin import constants
from fastapi_admin.depends import get_redis
from fastapi_admin.template import templates


class LoginProvider:
    def __init__(self, login_path="/login", logout_path="/logout", template="login.html"):
        self.template = template
        self.logout_path = logout_path
        self.login_path = login_path

    async def get(
        self,
        request: Request,
    ):
        return templates.TemplateResponse(self.template, context={"request": request})

    async def post(
        self,
        request: Request,
    ):
        """
        Post login
        :param request:
        :return:
        """

    async def authenticate(
        self,
        request: Request,
        call_next: Callable,
    ):
        response = await call_next(request)
        return response

    def redirect_login(self, request: Request):
        return RedirectResponse(
            url=request.app.admin_path + self.login_path, status_code=HTTP_303_SEE_OTHER
        )

    async def logout(self, request: Request):
        return self.redirect_login(request)


class UserMixin(Model):
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)

    class Meta:
        abstract = True


class UsernamePasswordProvider(LoginProvider):
    access_token = "access_token"

    def __init__(
        self,
        user_model: Type[UserMixin],
        login_path="/login",
        logout_path="/logout",
        template="login.html",
    ):
        super().__init__(login_path, logout_path, template)
        self.user_model = user_model

    async def post(self, request: Request, redis: Redis = Depends(get_redis)):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        remember_me = form.get("remember_me")

        user = await self.user_model.get_or_none(username=username)
        if not user or not self.check_password(user, password):
            return templates.TemplateResponse(
                self.template,
                status_code=HTTP_401_UNAUTHORIZED,
                context={"request": request, "error": _("login_failed")},
            )
        response = RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)
        if remember_me == "on":
            expire = 3600 * 24 * 30
            response.set_cookie("remember_me", "on")
        else:
            expire = 3600
            response.delete_cookie("remember_me")
        token = uuid.uuid4().hex
        response.set_cookie(
            self.access_token,
            token,
            expires=expire,
            path=request.app.admin_path,
            httponly=True,
        )
        await redis.set(constants.LOGIN_USER.format(token=token), user.pk, expire=expire)
        return response

    async def logout(self, request: Request, redis: Redis = Depends(get_redis)):
        response = await super(UsernamePasswordProvider, self).logout(request)
        response.delete_cookie(self.access_token)
        token = request.cookies.get(self.access_token)
        await redis.delete(constants.LOGIN_USER.format(token=token))
        return response

    async def authenticate(
        self,
        request: Request,
        call_next: Callable,
    ):
        redis = request.app.redis  # type:Redis
        token = request.cookies.get(self.access_token)
        path = request.scope["path"]
        token_key = constants.LOGIN_USER.format(token=token)
        user_id = await redis.get(token_key)
        if not user_id and path != self.login_path:
            return self.redirect_login(request)
        user = await self.user_model.get_or_none(pk=user_id)
        if not user:
            if path != self.login_path:
                response = self.redirect_login(request)
                response.delete_cookie(self.access_token)
                return response
        else:
            if path == self.login_path:
                return RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)
        request.state.user = user

        response = await call_next(request)
        return response

    def check_password(self, user: UserMixin, password: str):
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def hash_password(self, password: str):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    async def create_user(self, username: str, password: str, email: EmailStr):
        return await self.user_model.create(
            username=username,
            password=self.hash_password(password),
            email=email,
        )

    async def update_password(self, user: UserMixin, password: str):
        user.password = self.hash_password(password)
        await user.save(update_fields=["password"])
