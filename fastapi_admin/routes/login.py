import jwt
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from ..common import pwd_context
from ..factory import app
from ..schemas import LoginIn
from ..shortcuts import get_object_or_404

router = APIRouter()


@router.post(
    '/login',
)
async def login(
        login_in: LoginIn
):
    user_model = app.user_model
    user = await get_object_or_404(user_model, username=login_in.username)
    if not user.is_active:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='User is not Active!')
    if not pwd_context.verify(login_in.password, user.password):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Incorrect Password!')
    ret = {
        'user': {
            'username': user.username,
            'is_superuser': user.is_superuser,

        },
        'token': jwt.encode({'user_id': user.pk}, app.admin_secret, algorithm='HS256')
    }
    return ret
