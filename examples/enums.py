from enum import IntEnum


class EnumMixin:
    @classmethod
    def choices(cls):
        raise NotImplementedError


class Status(EnumMixin, IntEnum):
    """
    状态
    """
    on = 1
    off = 0

    @classmethod
    def choices(cls):
        return {
            cls.on: '开启',
            cls.off: '关闭'
        }


class BaiduAiCategory(EnumMixin, IntEnum):
    id_card = 1
    censor = 2

    @classmethod
    def choices(cls):
        return {
            cls.id_card: '身份证',
            cls.censor: '审核'
        }


class AliYunSecretCategory(EnumMixin, IntEnum):
    sms = 1
    oss = 2
    alert = 3

    @classmethod
    def choices(cls):
        return {
            cls.sms: '短信',
            cls.oss: 'oss',
            cls.alert: '报警'
        }


class DeviceSys(EnumMixin, IntEnum):
    android = 1
    ios = 2

    @classmethod
    def choices(cls):
        return {
            cls.android: '安卓',
            cls.ios: 'iOS',
        }
