from fastapi_admin.models import AbstractAdmin
from fastapi_admin.providers.login import UsernamePasswordProvider


class LoginProvider(UsernamePasswordProvider):
    async def update_password(self, admin: AbstractAdmin, password: str):
        pass
