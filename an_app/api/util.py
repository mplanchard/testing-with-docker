"""Common utilities."""

from functools import partial
from typing import Any, Callable, Iterable, Type

from aiohttp import web as aio_web


def map_endpoint_routes(
    web,
    endpoint: str,
    funcs: Iterable[Callable[[Any, aio_web.Request], aio_web.Response]],
) -> Iterable[aio_web.RouteDef]:
    """Return a mapping of routes for REST handlers for an endpoint."""
    return map(
        lambda f: getattr(web, f.__name__)(endpoint, partial(f, web)),
        funcs,
    )
