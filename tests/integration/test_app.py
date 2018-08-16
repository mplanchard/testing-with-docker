"""Tests for the app."""

from subprocess import Popen
from sys import executable
from time import sleep

import requests
import pytest
from sqlalchemy.dialects import postgresql
from sqlalchemy import text

from an_app.app import application
from an_app.db import pg_compile


class TestApp:

    @pytest.fixture(scope='class', autouse=True)
    def run_app(self):
        """Run the app for testing."""
        proc = Popen((executable, '-m', 'an_app.main'))
        sleep(1)
        yield
        proc.terminate()

    @pytest.fixture()
    async def app(self):
        """Return an instantiated application instance."""
        return await application()

    @pytest.fixture()
    async def users(self, app):
        """Add some users to the DB."""
        print(await app['db'].fetch('SELECT current_database()'))
        statements = [
            app['tables']['user'].insert().values(
                id=1, email='foo@foo.com', password='hashed!'
            ),
            app['tables']['user'].insert().values(
                id=2, email='bar@bar.com', password='hashed!'
            ),
            app['tables']['user'].insert().values(
                id=3, email='baz@baz.com', password='hashed!'
            ),
        ]
        for statement in statements:
            await app['db'].execute(str(pg_compile(statement)))
        yield
        await app['db'].execute(str(app['tables']['user'].delete()))

    def test_root(self):
        """Ensure we can get the root of the application."""
        resp = requests.get('http://localhost:8080/')
        assert resp.json() == {'text': 'hello, world!'}

    def test_users(self, users):
        """Ensure we get a list of users."""
        resp = requests.get('http://localhost:8080/users')
        assert len(resp.json()) == 3
