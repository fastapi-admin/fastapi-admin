import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from fastapi_admin.factory import app as admin_app
from fastapi_admin.site import Site, Menu

TORTOISE_ORM = {
    'connections': {
        'default': 'mysql://root:123456@127.0.0.1:3306/micro'
    },
    'apps': {
        'models': {
            'models': ['examples.models'],
            'default_connection': 'default',
        }
    }
}


def create_app():
    fast_app = FastAPI()

    register_tortoise(fast_app, config=TORTOISE_ORM)

    fast_app.mount('/admin', admin_app)

    admin_app.init(
        user_model='User',
        admin_secret='test',
        models='examples.models',
        site=Site(
            name='微服务管理后台',
            logo='https://github.com/long2ice/fastapi-admin/raw/master/front/static/img/logo.png',
            locale='zh-CN',
            locale_switcher=False,
            menu=[
                Menu(
                    name='首页',
                    url='/',
                    icon='fa fa-home'
                ),
                Menu(
                    name='配置',
                    title=True
                ),
                Menu(
                    name='应用',
                    url='/rest/App',
                    icon='fa fa-pencil'
                ),
                Menu(
                    name='阿里云秘钥',
                    url='/rest/AliYunSecret',
                    icon='fa fa-user-secret'
                ),
                Menu(
                    name='阿里云OSS',
                    url='/rest/AliYunOss',
                    icon='fa fa-database'
                ),
                Menu(
                    name='App短信',
                    url='/rest/AppSms',
                    icon='fa fa-envelope-o'
                ),
                Menu(
                    name='百度AI',
                    url='/rest/BaiduAi',
                    icon='fa fa-desktop'
                ),
                Menu(
                    name='App百度AI',
                    url='/rest/AppBaiduAi',
                    icon='fa fa-laptop',
                ),
                Menu(
                    name='在线参数',
                    url='/rest/Config',
                    icon='fa fa-cog'
                ),
                Menu(
                    name='基本信息',
                    title=True
                ),
                Menu(
                    name='请求日志',
                    url='/rest/ApiLog',
                    icon='fa fa-sticky-note'
                ),
                Menu(
                    name='App版本',
                    url='/rest/AppVersion',
                    icon='fa fa-mobile'
                ),
                Menu(
                    name='授权',
                    title=True
                ),
                Menu(
                    name='用户',
                    url='/rest/User',
                    icon='fa fa-user'
                ),
                Menu(
                    name='注销',
                    url='/login',
                    icon='fa fa-lock'
                )
            ]
        )
    )

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    return fast_app


app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, debug=True, reload=True)
