from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value


class Method(StrEnum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
    PATCH = "PATCH"
