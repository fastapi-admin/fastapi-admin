import os
from typing import List

from examples import enums
from examples.constants import BASE_DIR
from examples.models import Admin, Category, Config, Product
from fastapi_admin.app import app
from fastapi_admin.providers.file_upload import FileUploadProvider
from fastapi_admin.resources import Action, Dropdown, Field, Link, Model
from fastapi_admin.widgets import displays, filters, inputs

upload_provider = FileUploadProvider(uploads_dir=os.path.join(BASE_DIR, "static", "uploads"))


@app.register
class Home(Link):
    label = "Home"
    icon = "fas fa-home"
    url = "/admin"


@app.register
class AdminResource(Model):
    label = "Admin"
    model = Admin
    icon = "fas fa-user"
    page_pre_title = "admin list"
    page_title = "admin model"
    filters = [
        filters.Search(
            name="username", label="Name", search_mode="contains", placeholder="Search for username"
        ),
        filters.Date(name="created_at", label="CreatedAt"),
    ]
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="email", label="Email", input_=inputs.Email()),
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload_provider=upload_provider),
        ),
        "created_at",
    ]
    can_create = False

    def get_actions(self) -> List[Action]:
        return []

    def get_bulk_actions(self) -> List[Action]:
        return []


@app.register
class Content(Dropdown):
    class CategoryResource(Model):
        label = "Category"
        model = Category
        fields = ["id", "name", "slug", "created_at"]

    class ProductResource(Model):
        label = "Product"
        model = Product
        filters = [
            filters.Enum(enum=enums.ProductType, name="type", label="ProductType"),
            filters.Datetime(name="created_at", label="CreatedAt"),
        ]
        fields = [
            "id",
            "name",
            "view_num",
            "sort",
            "is_reviewed",
            "type",
            Field(name="image", label="Image", display=displays.Image(width="40")),
            "body",
            "created_at",
        ]

    label = "Content"
    icon = "fas fa-bars"
    resources = [ProductResource, CategoryResource]


@app.register
class ConfigResource(Model):
    label = "Config"
    model = Config
    icon = "fas fa-cogs"
    filters = [
        filters.Enum(enum=enums.Status, name="status", label="Status"),
        filters.Search(name="key", label="Key", search_mode="equal"),
    ]
    fields = [
        "id",
        "label",
        "key",
        "value",
        Field(
            name="status",
            label="Status",
            input_=inputs.RadioEnum(enums.Status, default=enums.Status.on),
        ),
    ]


@app.register
class GithubLink(Link):
    label = "Github"
    url = "https://github.com/fastapi-admin/fastapi-admin"
    icon = "fab fa-github"
    target = "_blank"


@app.register
class DocumentationLink(Link):
    label = "Documentation"
    url = "https://long2ice.github.io/fastadmin"
    icon = "fas fa-file-code"
    target = "_blank"
