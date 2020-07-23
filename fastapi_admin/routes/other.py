from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_409_CONFLICT

from fastapi_admin.common import pwd_context
from fastapi_admin.depends import get_current_user
from fastapi_admin.schemas import UpdatePasswordIn

router = APIRouter()


@router.put("/password")
async def update_password(update_password_in: UpdatePasswordIn, user=Depends(get_current_user)):
    if update_password_in.new_password != update_password_in.confirm_password:
        raise HTTPException(HTTP_409_CONFLICT, detail="Incorrect Confirm Password!")
    if not pwd_context.verify(update_password_in.old_password, user.password):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Incorrect Password!")
    user.password = pwd_context.hash(update_password_in.new_password)
    await user.save(update_fields=["password"])
    return {"success": True}
