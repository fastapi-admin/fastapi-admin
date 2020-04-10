import jwt
import orjson
from fastapi import Query, Path, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from .factory import app

auth_schema = HTTPBearer()


async def jwt_required(request: Request, token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    credentials_exception = HTTPException(HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token.credentials, app.admin_secret)
        user_id = payload.get('user_id')
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    request.scope['user_id'] = user_id
    return user_id


class QueryItem(BaseModel):
    page: int = 1
    sort: dict
    where: dict
    with_: dict
    size: int = 10
    sort: dict = {}

    class Config:
        fields = {
            'with_': 'with'
        }


def get_query(query=Query(...)):
    query = orjson.loads(query)
    return QueryItem.parse_obj(query)


def get_model(resource: str = Path(...)):
    model = getattr(app.models, resource)
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
