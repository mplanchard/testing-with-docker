"""Run the application."""

from aiohttp import web

from .app import application


web.run_app(application(), host='localhost', port='8080')
