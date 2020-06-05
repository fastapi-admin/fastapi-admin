from fastapi import Depends

from ..depends import jwt_required
from ..factory import app
from . import rest, site

app.include_router(site.router)
app.include_router(rest.router, dependencies=[Depends(jwt_required)], prefix="/rest")
