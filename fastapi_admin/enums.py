import abc
from enum import IntEnum


class EnumMixin:
    @classmethod
    @abc.abstractmethod
    def choices(cls):
        pass


class PermissionAction(EnumMixin, IntEnum):
    create = 1
    delete = 2
    update = 3
    read = 4

    @classmethod
    def choices(cls):
        return {
            cls.create: "Create",
            cls.delete: "Delete",
            cls.update: "Update",
            cls.read: "Read",
        }
