import os

from setuptools import find_packages, setup
from fastapi_admin import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()


def requirements():
    return open('requirements.txt', 'rt').read().splitlines()


setup(
    name='fastapi-admin',
    version=__version__,
    description='Fast Admin Dashboard based on fastapi and tortoise-orm and rest-admin.',
    author='long2ice',
    long_description_content_type='text/x-rst',
    long_description=long_description,
    author_email='long2ice@gmail.com',
    url='https://github.com/long2ice/fastapi-admin',
    license='MIT License',
    packages=find_packages(include=['fastapi_admin*']),
    include_package_data=True,
    platforms='any',
    keywords=(
        'fastapi admin dashboard'
    ),
    dependency_links=['https://github.com/long2ice/tortoise-orm.git@long2ice#egg=tortoise-orm'],
    install_requires=requirements(),
)
