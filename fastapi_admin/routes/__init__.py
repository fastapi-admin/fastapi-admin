from fastapi import Depends

from . import login, other, index
from ..depends import jwt_required
from ..factory import app

app.include_router(login.router)
app.include_router(other.router, dependencies=[Depends(jwt_required)])
app.include_router(index.router, dependencies=[Depends(jwt_required)])
