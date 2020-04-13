from tortoise import fields, Model

from fastapi_admin.models import User as AdminUser
from .enums import ProductType


class User(AdminUser, Model):
    last_login = fields.DatetimeField(description='Last Login')
    is_active = fields.BooleanField(default=True, description='Is Active')
    avatar = fields.CharField(max_length=200)
    intro = fields.TextField()
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
