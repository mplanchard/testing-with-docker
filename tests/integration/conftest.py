"""Test session configuration."""

from os import chdir, environ, path
from subprocess import Popen
from time import sleep, time

import pytest


@pytest.fixture(scope='session', autouse=True)
def setup_env():
    """Set the database name for the test session."""
    environ['DB_NAME'] = 'an_app_{}'.format(int(time()))
    # Level 2: we run our tests against their own dockerized pg instance
    environ['DB_PORT'] = '5433'


# Level 3: we build our image for each integration test run, and run
#          our integration tests against the built image.
@pytest.fixture(scope='session', autouse=True)
def build_image():
    """Build an image to test against."""
    root_dir = path.abspath(path.join(path.dirname(__file__)), '../..')
    Popen(
        ('docker', 'build', '.', '--tag', 'an_app:test'),
        cwd=root_dir,
    ).communicate()


@pytest.fixture(scope='session', autouse=True)
# def run_docker():
# Level 2: we set a unique DB test name and port for tests
# Level 3: we also
def run_docker(setup_env, build_image):
    """Run docker containers for integration tests."""
    this_dir = path.abspath(path.dirname(__file__))
    Popen(('docker-compose', 'up', '-d'), cwd=this_dir).communicate()
    sleep(5)
    yield
    Popen(('docker-compose', 'down', '-v'), cwd=this_dir).communicate()
