from enum import IntEnum
from fastapi_admin.enum import EnumMixin
from tortoise import fields

from fastapi_admin.models import User


class Status(EnumMixin, IntEnum):
    on = 1
    off = 2

    @classmethod
    def choices(cls):
        return {
            cls.on: 'ON',
            cls.off: 'OFF'
        }


class TestUser(User):
    is_active = fields.BooleanField(default=False, description='Is Active')
    status = fields.IntEnumField(Status, description='User Status')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
