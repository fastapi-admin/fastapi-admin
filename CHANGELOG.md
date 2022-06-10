# ChangeLog

## 1.0

### 1.0.4

- Add `widgets.filters.Boolean` class
- Fix multiple json field input. (#98)
- Fix `jinja2.ext.autoescape` error.

### 1.0.3

- Fix action link.
- Fix `get_m2m_field`.
- Refactor `ComputeField` and remove `get_compute_fields`.
- Upgrade `aioredis` to `2.0`.
- Make `get_current_admin` error to `401` and add `401` error page.

### 1.0.2

- Use `str` type for `pk` path param. (#52)
- Fix `Image` input.
- `filters` can accept `str` type and default use `Search` filter.
- Fix accessible when not login. (#53)

### 1.0.1

- Add `column_attributes`.
- Remove `can_create` and add `get_toolbar_actions`.
- Add `DistinctColumn` filter.
- Fix datetime filter.
- Add `resource.get_compute_fields`.
- Fix `init` admin.

### 1.0.0

**This is a completely different version and rewrite all code. If you are using old version, you can't upgrade directly,
but completely rewrite your code. So just consider try it in your new project.**

## 0.3

### 0.3.3

- Fix latest tortoise error.
- Fix home menu and update version.
- Only show action buttons if user has permission.

### 0.3.2

- Hide menu when no children menu.
- Add custom filters.

### 0.3.1

- Auto register permission.
- Add admin log.
- Add file import.

### 0.3.0

- Search_fields not required.
- Bug fix.
- Add `_rowVariant` and `_cellVariants`.
- Add update password.
- Fix user create password hash.
- Make `Role`,`Permission` abstract.

## 0.2

### 0.2.9

- Rename `fastapi_admin.models.User` to `fastapi_admin.models.AbstractUser`.
- Move `is_superuser` and `is_active` to base `AbstractUser`.
- Fix `createsuperuser` error.

### 0.2.8

- Add password auto hash.
- `Field` description as help text for form.
- Make `uvloop` dependency optional.

### 0.2.7

- Add custom login_view.

### 0.2.6

- Fix createsuperuser error.
- Update cli.

### 0.2.5

- Now there has builtin menus.
- Fix field type.
