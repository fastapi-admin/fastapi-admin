from tortoise import Model, fields

from fastapi_admin import enums


class User(Model):
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=200)

    class Meta:
        abstract = True


class Permission(Model):
    label = fields.CharField(max_length=50)
    model = fields.CharField(max_length=50)
    action: enums.PermissionAction = fields.IntEnumField(enums.PermissionAction, default=enums.PermissionAction.read)

    def __str__(self):
        return self.label


class Role(Model):
    label = fields.CharField(max_length=50)
    users = fields.ManyToManyField('models.User')

    permissions: fields.ManyToManyRelation[Permission] = fields.ManyToManyField('models.Permission')

    def __str__(self):
        return self.label
