from examples.models import User
from fastapi_admin.providers.login import UsernamePasswordProvider


class Login(UsernamePasswordProvider):
    model = User
