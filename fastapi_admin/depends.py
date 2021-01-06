import json

import jwt
from fastapi import Depends, HTTPException, Path, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from . import enums
from .factory import app

auth_schema = HTTPBearer()


async def jwt_required(
    request: Request, token: HTTPAuthorizationCredentials = Depends(auth_schema)
):
    credentials_exception = HTTPException(HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token.credentials, app.admin_secret, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    request.scope["user_id"] = user_id
    return user_id


async def jwt_optional(request: Request):
    authorization: str = request.headers.get("Authorization")
    scheme, credentials = get_authorization_scheme_param(authorization)
    if credentials:
        try:
            payload = jwt.decode(credentials, app.admin_secret, algorithms=["HS256"])
            user_id = payload.get("user_id")
            request.scope["user_id"] = user_id
            return user_id
        except jwt.PyJWTError:
            pass
    return


class QueryItem(BaseModel):
    page: int = 1
    sort: dict
    where: dict = {}
    with_: dict = {}
    size: int = 10
    sort: dict = {}

    class Config:
        fields = {"with_": "with"}


def get_query(query=Query(...)):
    query = json.loads(query)
    return QueryItem.parse_obj(query)


def get_model(resource: str = Path(...)):
    model = app.models.get(resource)
    return model


async def parse_body(request: Request, resource: str = Path(...)):
    body = await request.json()
    resource = await app.get_resource(resource, exclude_pk=True, exclude_m2m_field=False)
    resource_fields = resource.resource_fields.keys()
    ret = {}
    for key in resource_fields:
        v = body.get(key)
        if v is not None:
            ret[key] = v
    return ret, resource_fields


async def get_current_user(user_id=Depends(jwt_required)):
    user = await app.user_model.get_or_none(pk=user_id)
    if not user:
        raise HTTPException(HTTP_404_NOT_FOUND)
    return user


class PermissionsChecker:
    def __init__(self, action: enums.PermissionAction):
        self.action = action

    async def __call__(self, resource: str = Path(...), user=Depends(get_current_user)):
        if not app.permission or user.is_superuser:
            return
        if not user.is_active:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN)
        has_permission = False
        await user.fetch_related("roles")
        for role in user.roles:
            if await role.permissions.filter(model=resource, action=self.action):
                has_permission = True
                break
        if not has_permission:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN)


read_checker = PermissionsChecker(action=enums.PermissionAction.read)
create_checker = PermissionsChecker(action=enums.PermissionAction.create)
update_checker = PermissionsChecker(action=enums.PermissionAction.update)
delete_checker = PermissionsChecker(action=enums.PermissionAction.delete)


class AdminLog:
    def __init__(self, action: str):
        self.action = action

    async def __call__(
        self, request: Request, resource: str = Path(...), admin_id=Depends(jwt_required),
    ):
        if app.admin_log:
            content = None
            if request.method in ["POST", "PUT"]:
                content = await request.json()
            elif request.method == "DELETE":
                content = {"pk": request.path_params.get("id")}
            if content:
                await app.admin_log_model.create(
                    admin_id=admin_id, action=self.action, model=resource, content=content
                )


admin_log_create = AdminLog(action="create")
admin_log_update = AdminLog(action="update")
admin_log_delete = AdminLog(action="delete")
