import os
import re

from setuptools import find_packages, setup


def version():
    ver_str_line = open('fastapi_admin/__init__.py', 'rt').read()
    mob = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", ver_str_line, re.M)
    if not mob:
        raise RuntimeError("Unable to find version string")
    return mob.group(1)


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()


def requirements():
    return open('requirements.txt', 'rt').read().splitlines()


setup(
    name='fastapi-admin',
    version=version(),
    description='Fast Admin Dashboard based on fastapi and tortoise-orm and rest-admin.',
    author='long2ice',
    long_description_content_type='text/x-rst',
    long_description=long_description,
    author_email='long2ice@gmail.com',
    url='https://github.com/long2ice/fastapi-admin',
    license='MIT License',
    packages=find_packages(include=['fastapi_admin*']),
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'console_scripts': ['fastapi-admin = fastapi_admin.cli:cli'],
    },
    platforms='any',
    keywords=(
        'fastapi admin dashboard'
    ),
    dependency_links=['https://github.com/long2ice/tortoise-orm.git@long2ice#egg=tortoise-orm'],
    install_requires=requirements(),
)
