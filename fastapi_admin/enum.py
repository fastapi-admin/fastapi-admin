import abc


class EnumMixin:
    @classmethod
    @abc.abstractmethod
    def choices(cls):
        pass
