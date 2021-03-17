from typing import Dict, List, Optional, Type

import jwt
from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from tortoise import Model

from . import enums
from .common import get_all_models, import_obj, pwd_context
from .exceptions import exception_handler
from .filters import SearchFilter
from .models import AbstractAdminLog, AbstractPermission, AbstractRole, AbstractUser
from .schemas import LoginIn
from .shortcuts import get_object_or_404
from .site import Field, Menu, Resource, Site


async def login(login_in: LoginIn):
    user_model = app.user_model
    user = await get_object_or_404(user_model, username=login_in.username)
    if not user.is_active:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User is not Active!")
    if not pwd_context.verify(login_in.password, user.password):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Incorrect Password!")
    ret = {
        "user": {
            "username": user.username,
            "is_superuser": user.is_superuser,
            "avatar": user.avatar if hasattr(user, "avatar") else None,
        },
        "token": jwt.encode({"user_id": user.pk}, app.admin_secret, algorithm="HS256"),
    }
    return ret


class AdminApp(FastAPI):
    models: Dict[str, Type[Model]] = {}
    admin_secret: str
    user_model: Type[Model]
    permission_model: Type[Model]
    role_model: Type[Model]
    admin_log_model: Type[Model]
    site: Site
    permission: bool
    admin_log: bool
    _inited: bool = False
    _field_type_mapping = {
        "IntField": "number",
        "BooleanField": "checkbox",
        "DatetimeField": "datetime",
        "DateField": "date",
        "IntEnumFieldInstance": "select",
        "CharEnumFieldInstance": "select",
        "DecimalField": "number",
        "FloatField": "number",
        "TextField": "textarea",
        "SmallIntField": "number",
        "JSONField": "json",
    }
    model_menu_mapping: Dict[str, Menu] = {}

    def _get_model_menu_mapping(self, menus: List[Menu]):
        for menu in filter(lambda x: (x.url and "rest" in x.url) or x.children, menus):
            if menu.children:
                self._get_model_menu_mapping(menu.children)
            else:
                self.model_menu_mapping[menu.url.split("?")[0].split("/")[-1]] = menu

    def _get_model_fields_type(self, model: Type[Model]) -> Dict:
        model_describe = model.describe()
        ret = {}
        data_fields = model_describe.get("data_fields")
        pk_field = model_describe.get("pk_field")
        fk_fields = model_describe.get("fk_fields")
        m2m_fields = model_describe.get("m2m_fields")
        fields = [pk_field] + data_fields + fk_fields + m2m_fields
        for field in fields:
            ret[field.get("name")] = self._get_field_type(
                field.get("name"), field.get("field_type")
            )
        return ret

    def _build_content_menus(self) -> List[Menu]:
        menus = []
        for model_name, model in get_all_models():
            if issubclass(model, (AbstractUser, AbstractPermission, AbstractRole)):
                continue
            menu = Menu(
                name=model._meta.table_description or model_name,
                url=f"/rest/{model_name}",
                fields_type=self._get_model_fields_type(model),
                icon="icon-list",
                bulk_actions=[{"value": "delete", "text": "delete_all"}],
            )
            menus.append(menu)
        return menus

    def _build_default_menus(self, permission=True):
        """
        build default menus when menus config not set
        :return:
        """

        menus = [
            Menu(name="Home", url="/", icon="fa fa-home"),
            Menu(name="Content", children=self._build_content_menus()),
            Menu(
                name="External",
                children=[
                    Menu(
                        name="Github",
                        url="https://github.com/long2ice/fastapi-admin",
                        icon="fa fa-github",
                        external=True,
                    ),
                ],
            ),
        ]
        if permission:
            permission_menus = [
                Menu(
                    name="Auth",
                    children=[
                        Menu(
                            name="User",
                            url="/rest/User",
                            icon="fa fa-user",
                            search_fields=("username",),
                        ),
                        Menu(name="Role", url="/rest/Role", icon="fa fa-group",),
                        Menu(name="Permission", url="/rest/Permission", icon="fa fa-user-plus",),
                        Menu(name="Logout", url="/logout", icon="fa fa-lock",),
                    ],
                ),
            ]
            menus += permission_menus
        return menus

    async def init(
        self,
        site: Site,
        admin_secret: str,
        permission: bool = False,
        admin_log: bool = False,
        login_view: Optional[str] = None,
    ):
        """
        init admin site
        :param admin_log:
        :param login_view:
        :param permission: active builtin permission
        :param site:
        :param admin_secret: admin jwt secret.
        :return:
        """
        self.site = site
        self.permission = permission
        self.admin_secret = admin_secret
        self.admin_log = admin_log
        for model_name, model in get_all_models():
            if issubclass(model, AbstractUser):
                self.user_model = model
            elif issubclass(model, AbstractAdminLog):
                self.admin_log_model = model
            self.models[model_name] = model
        self._inited = True
        if not site.menus:
            site.menus = self._build_default_menus(permission)
        if permission:
            await self._register_permissions()
        self._get_model_menu_mapping(site.menus)
        if login_view:
            self.add_api_route("/login", import_obj(login_view), methods=["POST"])
        else:
            self.add_api_route("/login", login, methods=["POST"])

    async def _register_permissions(self):
        permission_model = None
        for model_name, model in get_all_models():
            if issubclass(model, AbstractPermission):
                permission_model = model
                break
        if not permission_model:
            raise Exception("No Permission Model Founded.")

        for model, _ in get_all_models():
            for action in enums.PermissionAction.choices():
                label = f"{enums.PermissionAction.choices().get(action)} {model}"
                defaults = dict(label=label, model=model, action=action,)
                await permission_model.get_or_create(**defaults,)

    def _exclude_field(self, resource: str, field: str):
        """
        exclude field by menu include and exclude
        :param resource:
        :param field:
        :return:
        """
        menu = self.model_menu_mapping[resource]
        if menu.include:
            if field not in menu.include:
                return True
        if menu.exclude:
            if field in menu.exclude:
                return True
        return False

    def _get_field_type(self, name: str, field_type: str, menu: Optional[Menu] = None) -> str:
        """
        get field display type
        :param menu:
        :param field_type:
        :return:
        """
        field_type = self._field_type_mapping.get(field_type) or "text"
        if menu:
            field_type = menu.fields_type.get(name) or field_type
        return field_type

    async def _build_resource_from_model_describe(
        self,
        resource: str,
        model: Type[Model],
        model_describe: dict,
        exclude_pk: bool,
        exclude_m2m_field=True,
        exclude_actions=False,
    ):
        """
        build resource
        :param resource:
        :param model:
        :param model_describe:
        :param exclude_pk:
        :param exclude_m2m_field:
        :return:
        """
        data_fields = model_describe.get("data_fields")
        pk_field = model_describe.get("pk_field")
        fk_fields = model_describe.get("fk_fields")
        m2m_fields = model_describe.get("m2m_fields")
        menu = self.model_menu_mapping[resource]
        search_fields_ret = {}
        search_fields = menu.search_fields
        sort_fields = menu.sort_fields
        fields = {}
        pk = name = pk_field.get("name")
        # CustomSearchFilters
        for search_filter in filter(
            lambda x: type(x).__name__ == "type" and issubclass(x, SearchFilter), search_fields
        ):
            search_fields_ret[search_filter.get_name()] = await search_filter.get_field()
        if not exclude_pk and not self._exclude_field(resource, name):
            field = Field(
                label=pk_field.get("name").title(),
                required=True,
                type=self._get_field_type(name, pk_field.get("field_type").__name__, menu),
                sortable=name in sort_fields,
                description=pk_field.get("description"),
            )
            field = field.copy(update=menu.attrs.get(name) or {})
            fields = {name: field}
        if not exclude_actions and menu.actions:
            fields["_actions"] = menu.actions

        for data_field in data_fields:
            readonly = data_field.get("constraints").get("readOnly")
            field_type = data_field.get("field_type").__name__
            name = data_field.get("name")
            if self._exclude_field(resource, name):
                continue

            type_ = self._get_field_type(name, field_type, menu)
            options = []
            if type_ == "select" or type_ == "radiolist":
                for k, v in model._meta.fields_map[name].enum_type.choices().items():
                    options.append({"text": v, "value": k})

            label = data_field.get("name").title()
            field = Field(
                label=label,
                required=not data_field.get("nullable"),
                type=type_,
                options=options,
                sortable=name in sort_fields,
                disabled=readonly,
                description=data_field.get("description"),
            )
            if field_type == "DecimalField" or field_type == "FloatField":
                field.step = "any"
            field = field.copy(update=menu.attrs.get(name) or {})
            fields[name] = field
            if name in search_fields:
                search_fields_ret[name] = field.copy(update=dict(required=False))

        for fk_field in fk_fields:
            name = fk_field.get("name")
            if not self._exclude_field(resource, name):
                if name not in menu.raw_id_fields:
                    fk_model_class = fk_field.get("python_type")
                    objs = await fk_model_class.all()
                    raw_field = fk_field.get("raw_field")
                    label = name.title()
                    options = list(map(lambda x: {"text": str(x), "value": x.pk}, objs))
                    field = Field(
                        label=label,
                        required=True,
                        type="select",
                        options=options,
                        sortable=name in sort_fields,
                        description=fk_field.get("description"),
                    )
                    field = field.copy(update=menu.attrs.get(name) or {})
                    fields[raw_field] = field
                    if name in search_fields:
                        search_fields_ret[raw_field] = field.copy(update=dict(required=False))
        if not exclude_m2m_field:
            for m2m_field in m2m_fields:
                name = m2m_field.get("name")
                if not self._exclude_field(resource, name):
                    label = name.title()
                    m2m_model_class = m2m_field.get("python_type")
                    objs = await m2m_model_class.all()
                    options = list(map(lambda x: {"text": str(x), "value": x.pk}, objs))
                    fields[name] = Field(
                        label=label,
                        type="tree",
                        options=options,
                        multiple=True,
                        description=m2m_field.get("description"),
                        **menu.attrs.get(name) or {},
                    )
        return pk, fields, search_fields_ret

    async def get_resource(
        self, resource: str, exclude_pk=False, exclude_m2m_field=True, exclude_actions=False
    ) -> Resource:
        if not self._inited:
            raise Exception("must call init() first!")
        model = self.models.get(resource)  # type:Type[Model]
        model_describe = model.describe(serializable=False)
        pk, fields, search_fields = await self._build_resource_from_model_describe(
            resource, model, model_describe, exclude_pk, exclude_m2m_field, exclude_actions
        )
        menu = self.model_menu_mapping[resource]
        return Resource(
            title=model_describe.get("description") or resource.title(),
            fields=fields,
            searchFields=search_fields,
            pk=pk,
            bulk_actions=menu.bulk_actions,
            export=menu.export,
            import_=menu.import_,
        )


app = AdminApp(
    debug=False,
    title="FastAPI-Admin",
    root_path="/admin",
    description="FastAPI Admin Dashboard based on FastAPI and Tortoise ORM.",
)
app.add_exception_handler(HTTPException, exception_handler)
