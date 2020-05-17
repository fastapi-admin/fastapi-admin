import datetime

from tortoise import fields, Model

from fastapi_admin.models import User as AdminUser
from .enums import ProductType, Status


class User(AdminUser):
    last_login = fields.DatetimeField(description='Last Login', default=datetime.datetime.now)
    is_active = fields.BooleanField(default=True, description='Is Active')
    is_superuser = fields.BooleanField(default=False, description='Is SuperUser')
    avatar = fields.CharField(max_length=200, default='')
    intro = fields.TextField(default='')
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}#{self.username}'


class Category(Model):
    slug = fields.CharField(max_length=200)
    name = fields.CharField(max_length=200)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}#{self.name}'


class Product(Model):
    categories = fields.ManyToManyField('models.Category')
    name = fields.CharField(max_length=50)
    view_num = fields.IntField(description='View Num')
    sort = fields.IntField()
    is_reviewed = fields.BooleanField(description='Is Reviewed')
    type = fields.IntEnumField(ProductType, description='Product Type')
    image = fields.CharField(max_length=200)
    body = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}#{self.name}'


class Config(Model):
    label = fields.CharField(max_length=200)
    key = fields.CharField(max_length=20)
    value = fields.JSONField()
    status: Status = fields.IntEnumField(Status, default=Status.on)

    def __str__(self):
        return f'{self.pk}#{self.label}'
