import jwt
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from passlib.context import CryptContext
from starlette.status import HTTP_403_FORBIDDEN

from ..factory import app
from ..schemas import LoginIn
from ..shortcuts import get_object_or_404

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter()


@router.post(
    '/login',
)
async def login(
        login_in: LoginIn
):
    user_model = app.user_model
    user = await get_object_or_404(user_model, username=login_in.username)
    if not pwd_context.verify(login_in.password, user.password):
        return ORJSONResponse(status_code=HTTP_403_FORBIDDEN, content={
            'message': 'Incorrect Password'
        })
    return {
        'user': {
            'username': user.username
        },
        'token': jwt.encode({'user_id': user.pk}, app.admin_secret, algorithm='HS256')
    }
