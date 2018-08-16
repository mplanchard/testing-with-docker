"""The main application."""

from copy import copy
from dotenv import dotenv_values
from os import environ, path
from typing import MutableMapping

from aiohttp import web

from .api import root, users
from .db import create_tables, get_connection, get_metadata, get_tables


def setenv(env: MutableMapping[str, str]) -> MutableMapping[str, str]:
    """Update the environment to contain our values."""
    env = copy(env)
    env['DB_USER'] = 'testuser'
    env['DB_PASS'] = 'testpass'
    env['DB_HOST'] = 'localhost'
    env['DB_PORT'] = '5432'
    env['DB_NAME'] = 'an_app'
    return env


# def setenv(
#     dotenv_path: str,
#     env: MutableMapping[str, str]
# ) -> MutableMapping[str, str]:
#     """Pull the dotenv and source the environment."""
#     denv = dotenv_values(dotenv_path=dotenv_path)
#     return {**denv, **env}
#     return env


async def application() -> web.Application:
    """Return an app server ready to be started."""
    # env = setenv(
    #     path.join(path.abspath(path.dirname(__file__)), '../.env'),
    #     environ
    # )
    env = setenv(environ)
    app = web.Application()
    app.add_routes(root.endpoints(web))
    app.add_routes(users.users_endpoints(web))
    app['db'] = await get_connection(env)
    metadata = get_metadata()
    app['tables'] = dict(get_tables(metadata))
    await create_tables(app['db'], metadata)
    return app
