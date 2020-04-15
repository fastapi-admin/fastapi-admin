import argparse
import importlib

from colorama import Fore, init
from prompt_toolkit import PromptSession
from tortoise import Tortoise, run_async

from fastapi_admin import enums
from fastapi_admin.common import pwd_context
from fastapi_admin.models import Permission

init(autoreset=True)


class Logger:
    @classmethod
    def success(cls, text):
        print(Fore.GREEN + text)

    @classmethod
    def waring(cls, text):
        print(Fore.YELLOW + text)

    @classmethod
    def error(cls, text):
        print(Fore.RED + text)


def import_obj(path):
    module_name, class_name = path.rsplit('.', 1)
    return getattr(importlib.import_module(module_name), class_name)


async def init_tortoise(args):
    await Tortoise.init(config=import_obj(args.config))


async def register_permissions(args):
    await init_tortoise(args)
    if args.clean:
        await Permission.all().delete()
        Logger.waring('Cleaned all permissions success.')
    models = Tortoise.apps.get('models').keys()
    models = list(models)
    for model in models:
        for action in enums.PermissionAction:
            label = f'{enums.PermissionAction.choices().get(action)} {model}'
            defaults = dict(
                label=label,
                model=model,
                action=action,
            )
            _, created = await Permission.get_or_create(
                **defaults,
            )
            if created:
                Logger.success(f'Create permission {label} success.')


async def createsuperuser(args):
    await init_tortoise(args)

    user_model = import_obj(args.user_model)
    prompt = PromptSession()
    while True:
        try:
            username = await prompt.prompt_async('Username: ')
            password = await prompt.prompt_async('Password: ', is_password=True)
            try:
                await user_model.create(
                    username=username,
                    password=pwd_context.hash(password),
                    is_superuser=True
                )
                Logger.success(f'Create superuser {username} success.')
                return
            except Exception as e:
                Logger.error(f'Create superuser {username} error,{e}')
        except (EOFError, KeyboardInterrupt):
            Logger.success(f'Exit success!')
            return


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands')
    parser.add_argument('-c', '--config', required=True,
                        help='Tortoise-orm config dict import path,like settings.TORTOISE_ORM.')

    parser_register_permissions = subparsers.add_parser('register_permissions')
    parser_register_permissions.add_argument('--clean', required=False, action='store_true',
                                             help='Clean up old permissions then renew.')
    parser_register_permissions.set_defaults(func=register_permissions)

    parser_createsuperuser = subparsers.add_parser('createsuperuser')
    parser_createsuperuser.add_argument('--user-model', required=True,
                                        help='User model import path,like examples.models.User.')
    parser_createsuperuser.set_defaults(func=createsuperuser)

    parse_args = parser.parse_args()
    run_async(parse_args.func(parse_args))


if __name__ == '__main__':
    cli()
