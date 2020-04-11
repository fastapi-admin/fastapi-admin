from typing import List

from fastapi import Body
from pydantic import BaseModel


class LoginIn(BaseModel):
    username: str = Body(..., example='long2ice')
    password: str = Body(..., example='123456')


class BulkIn(BaseModel):
    pk_list: List = Body(..., example=[1, 2, 3])
