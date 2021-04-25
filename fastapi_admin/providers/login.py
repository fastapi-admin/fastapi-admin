from gettext import gettext as _
from typing import Callable, Type

import bcrypt
from pydantic import EmailStr
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from tortoise import Model, fields

from fastapi_admin.template import templates


class LoginProvider:
    login_path = "/login"
    logout_path = "/logout"
    template = "login.html"

    @classmethod
    async def get(
        cls,
        request: Request,
    ):
        return templates.TemplateResponse(cls.template, context={"request": request})

    @classmethod
    async def post(
        cls,
        request: Request,
    ):
        """
        Post login
        :param request:
        :return:
        """

    @classmethod
    async def authenticate(
        cls,
        request: Request,
        call_next: Callable,
    ):
        response = await call_next(request)
        return response

    @classmethod
    async def logout(cls, request: Request):
        return RedirectResponse(
            url=request.app.admin_path + cls.login_path, status_code=HTTP_303_SEE_OTHER
        )


class UserMixin(Model):
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)

    class Meta:
        abstract = True


class UsernamePasswordProvider(LoginProvider):
    model: Type[UserMixin]

    @classmethod
    async def post(
        cls,
        request: Request,
    ):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        user = await cls.model.get_or_none(username=username)
        if not user:
            return templates.TemplateResponse(
                cls.template, context={"request": request, "error": _("no_such_user")}
            )
        if not cls.check_password(user, password):
            return templates.TemplateResponse(
                cls.template, context={"request": request, "error": _("password_error")}
            )
        return RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)

    @classmethod
    def check_password(cls, user: UserMixin, password: str):
        return bcrypt.checkpw(password.encode(), user.password.encode())

    @classmethod
    def hash_password(cls, password: str):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @classmethod
    async def create_user(cls, username: str, password: str, email: EmailStr):
        return await cls.model.create(
            username=username,
            password=cls.hash_password(password),
            email=email,
        )

    @classmethod
    async def update_password(cls, user: UserMixin, password: str):
        user.password = cls.hash_password(password)
        await user.save(update_fields=["password"])
