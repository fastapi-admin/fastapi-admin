import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from fastapi_admin.factory import app as admin_app
from fastapi_admin.site import Site, Menu

TORTOISE_ORM = {
    'connections': {
        'default': 'mysql://root:123456@127.0.0.1:3306/test'
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
        user_model='TestUser',
        admin_secret='test',
        models='examples.models',
        site=Site(
            name='FastAPI-Admin',
            logo='https://avatars2.githubusercontent.com/u/13377178?s=460&u=d150d522579f41a52a0b3dd8ea997e0161313b6e&v=4',
            locale='en-US',
            locale_switcher=True,
            menu=[
                Menu(
                    name='Home',
                    url='/home',
                    icon='fa fa-home',
                ),
                Menu(
                    name='Information',
                    title=True,
                    icon='fa fa-user',
                ),
                Menu(
                    name='User',
                    url='/rest/TestUser',
                    icon='fa fa-user',
                ),
                Menu(
                    name='Logout',
                    url='/logout',
                    icon='icon-lock',
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
