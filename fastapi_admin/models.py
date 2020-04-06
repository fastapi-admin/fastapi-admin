from tortoise import Model, fields


class User(Model):
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=200)

    class Meta:
        abstract = True
