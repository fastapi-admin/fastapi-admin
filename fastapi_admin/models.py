from tortoise import Model, fields


class AbstractAdmin(Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)

    class Meta:
        abstract = True
