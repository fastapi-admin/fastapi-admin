from typing import List, Optional, Type

from fastapi import Depends
from fastapi.params import Path
from starlette.requests import Request
from tortoise import Tortoise

from fastapi_admin.exceptions import InvalidResource
from fastapi_admin.resources import Dropdown, Link, Model, Resource


def get_model(resource: Optional[str] = Path(...)):
    if not resource:
        return
    for app, models in Tortoise.apps.items():
        model = models.get(resource.title())
        if model:
            return model


def get_model_resource(request: Request, model=Depends(get_model)):
    return request.app.get_model_resource(model)


def _get_resources(resources: List[Type[Resource]]):
    ret = []
    for resource in resources:
        item = {
            "icon": resource.icon,
            "label": resource.label,
        }
        if issubclass(resource, Link):
            item["type"] = "link"
            item["url"] = resource.url
            item["target"] = resource.target
        elif issubclass(resource, Model):
            item["type"] = "model"
            item["model"] = resource.model.__name__.lower()
        elif issubclass(resource, Dropdown):
            item["type"] = "dropdown"
            item["resources"] = _get_resources(resource.resources)
        else:
            raise InvalidResource("Should be subclass of Resource")
        ret.append(item)
    return ret


def get_resources(request: Request) -> List[dict]:
    resources = request.app.resources
    return _get_resources(resources)
