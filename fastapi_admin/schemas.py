from fastapi import Body
from pydantic import BaseModel


class LoginIn(BaseModel):
    username: str = Body(..., example='long2ice')
    password: str = Body(..., example='123456')
