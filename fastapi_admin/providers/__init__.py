import typing

if typing.TYPE_CHECKING:
    from fastapi_admin.app import FastAPIAdmin


class Provider:
    name = "provider"

    async def register(self, app: "FastAPIAdmin"):
        setattr(app, self.name, self)
