import argparse
import sys

from colorama import Fore, init
from prompt_toolkit import PromptSession
from tortoise import Tortoise, run_async

from fastapi_admin import version
from fastapi_admin.common import import_obj, pwd_context

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


async def init_tortoise(args):
    await Tortoise.init(config=import_obj(args.config))


async def createsuperuser(args):
    await init_tortoise(args)

    user_model = Tortoise.apps.get("models").get(args.user)
    prompt = PromptSession()
    while True:
        try:
            username = await prompt.prompt_async("Username: ")
            password = await prompt.prompt_async("Password: ", is_password=True)
            try:
                await user_model.create(
                    username=username, password=pwd_context.hash(password), is_superuser=True
                )
                Logger.success(f"Create superuser {username} success.")
                return
            except Exception as e:
                Logger.error(f"Create superuser {username} error,{e}")
        except (EOFError, KeyboardInterrupt):
            Logger.success("Exit success!")
            return


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="subcommands")
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help="Tortoise-orm config dict import path,like settings.TORTOISE_ORM.",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"fastapi-admin version, {version()}",
        help="show the version",
    )

    parser_createsuperuser = subparsers.add_parser("createsuperuser")
    parser_createsuperuser.add_argument(
        "-u", "--user", required=True, help="User model name, like User or Admin."
    )
    parser_createsuperuser.set_defaults(func=createsuperuser)

    parse_args = parser.parse_args()
    run_async(parse_args.func(parse_args))


def main():
    sys.path.insert(0, ".")
    cli()
