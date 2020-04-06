from tortoise import fields, Model


class BaseModel(Model):
    create_at = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_at = fields.DatetimeField(auto_now=True, description='更新时间')

    class Meta:
        abstract = True
