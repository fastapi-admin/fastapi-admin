from tortoise import Model, fields

from fastapi_admin import enums


class AbstractUser(Model):
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(
        max_length=200, description="Will auto hash with raw password when change"
    )
    is_active = fields.BooleanField(default=True,)
    is_superuser = fields.BooleanField(default=False)

    class Meta:
        abstract = True


class AbstractPermission(Model):
    label = fields.CharField(max_length=50)
    model = fields.CharField(max_length=50)
    action: enums.PermissionAction = fields.IntEnumField(
        enums.PermissionAction, default=enums.PermissionAction.read
    )

    def __str__(self):
        return self.label

    class Meta:
        abstract = True


class AbstractRole(Model):
    label = fields.CharField(max_length=50)
    users = fields.ManyToManyField("models.User")

    permissions = fields.ManyToManyField("models.Permission")

    def __str__(self):
        return self.label

    class Meta:
        abstract = True


class AbstractAdminLog(Model):
    admin_log_id = fields.IntField(pk=True)
    admin = fields.ForeignKeyField("models.User")
    action = fields.CharField(max_length=20)
    model = fields.CharField(max_length=50)
    content = fields.JSONField()

    class Meta:
        abstract = True
