"""Define user endpoints for the application."""

from typing import List

from aiohttp import web as aio_web
from sqlalchemy import select

from .util import map_endpoint_routes


def users_endpoints(web) -> List[aio_web.RouteDef]:
    """Create and return a list of root endpoints."""
    async def get(web, request: aio_web.Request) -> aio_web.Response:
        """Respond to get requests."""
        users = await request.app['db'].fetch(
            str(select([request.app['tables']['user']]))
        )
        return web.json_response(list(map(
            lambda u: dict(u),
            users,
        )))

    return list(map_endpoint_routes(web, '/users', (get,)))
