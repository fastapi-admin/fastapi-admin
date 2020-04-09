from tortoise import fields

from . import BaseModel
from .enums import AliYunSecretCategory, BaiduAiCategory, Status, DeviceSys
from fastapi_admin.models import User as AdminUser


class User(AdminUser, BaseModel):
    last_login = fields.DatetimeField(description='上次登录')

    def __str__(self):
        return f'{self.pk}#{self.username}'


class AliYunSecret(BaseModel):
    app_id = fields.CharField(max_length=50)
    app_secret = fields.CharField(max_length=50)
    category = fields.IntEnumField(AliYunSecretCategory, description='类别', default=AliYunSecretCategory.sms)


class AliYunOss(BaseModel):
    bucket = fields.CharField(max_length=50, unique=True, description='仓库')
    domain = fields.CharField(max_length=200, description='域名')
    endpoint = fields.CharField(max_length=200, description='端点')
    aliyun_secret = fields.ForeignKeyField('models.AliYunSecret', related_name='aliyunoss')


class App(BaseModel):
    uaid = fields.IntField(unique=True)
    label = fields.CharField(max_length=20)
    secret = fields.CharField(max_length=16, description='通信密钥')
    work_secret = fields.CharField(max_length=100, description='企业微信密钥')

    def __str__(self):
        return f'{self.uaid}#{self.label}'


class AppSms(BaseModel):
    app = fields.ForeignKeyField('models.App', related_name='app_sms')
    scene = fields.CharField(max_length=50, description='使用场景')
    aliyun_secret = fields.ForeignKeyField('models.AliYunSecret', related_name='app_sms')
    sign_name = fields.CharField(max_length=20, description='签名')
    template_code = fields.CharField(max_length=20, description='模板编号')

    class Meta:
        unique_together = (('app', 'scene'),)


class BaiduAi(BaseModel):
    app_id = fields.CharField(max_length=50)
    api_key = fields.CharField(max_length=50)
    app_secret = fields.CharField(max_length=50)
    category = fields.IntEnumField(BaiduAiCategory, description='应用类别', default=BaiduAiCategory.id_card)

    def __str__(self):
        return f'{self.pk}#{self.app_id}'


class AppBaiduAi(BaseModel):
    app = fields.ForeignKeyField('models.App', related_name='app_baidu_ais')
    baidu_ai = fields.ForeignKeyField('models.BaiduAi', related_name='app_baidu_ais')


class Config(BaseModel):
    label = fields.CharField(max_length=200)
    key = fields.CharField(max_length=20)
    value = fields.JSONField()
    status: Status = fields.IntEnumField(Status, default=Status.on, description='状态')


class ApiLog(BaseModel):
    app = fields.ForeignKeyField('models.App', related_name='api_logs')
    endpoint = fields.CharField(max_length=50)
    success = fields.BooleanField(default=True, description='是否成功')
    status_code = fields.SmallIntField(description='状态码')


class AppVersion(BaseModel):
    app = fields.ForeignKeyField('models.App', related_name='app_versions')
    channel = fields.CharField(max_length=20, description='渠道')
    device_sys = fields.IntEnumField(DeviceSys, default=DeviceSys.android, description='操作系统')
    version_code = fields.CharField(max_length=20, description='版本号')
    describe = fields.CharField(max_length=200, description='描述')
    download_url = fields.CharField(max_length=200, description='下载链接')
    is_update = fields.BooleanField(default=False, description='是否更新')

    class Meta:
        ordering = ['-id']
        indexes = (('app', 'device_sys', 'channel'),)


class ManyToManyTest(BaseModel):
    apps = fields.ManyToManyField('models.App')
    label = fields.CharField(max_length=200)
