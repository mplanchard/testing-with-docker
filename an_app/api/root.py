"""Define root level endpoints for the application."""

from typing import List

from aiohttp import web as aio_web

from .util import map_endpoint_routes


def endpoints(web) -> List[aio_web.RouteDef]:
    """Create and return a list of root endpoints."""
    async def get(web, request: aio_web.Request) -> aio_web.Response:
        """Respond to get requests."""
        return web.json_response({'text': 'hello, world!'})

    return list(map_endpoint_routes(web, '/', (get,)))
