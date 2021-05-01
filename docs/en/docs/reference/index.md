# Configuration

The following configurations can be used to `admin_app.configure(...)`.

## logo_url

Will show the logo image in admin dashboard.

## login_logo_url

Will show the logo in login page.

## admin_path

Default is `/admin`, but you can change to other page.

## maintenance (💗 Pro only)

If set to `true`, all pages will be redirected to the `/maintenance` page.

## redis

Instance of `aioredis`.

## default_locale

Current support `zh` and `en`, default is `en`.

## template_folders

Template folders used to override builtin templates.

## login_provider

You can pass subclasses of `fastapi_admin.providers.login.LoginProvider`, there is a builtin `fastapi_admin.providers.login.UsernamePasswordProvider` you can use.

### user_model

Subclass instance of `fastapi_admin.providers.login.UserMixin`.

### enable_captcha (💗 Pro only)

Show captcha in admin login page.
