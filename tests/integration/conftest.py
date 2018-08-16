"""Test session configuration."""

from os import chdir, environ, path
from subprocess import Popen
from time import sleep, time

import pytest


# @pytest.fixture(scope='session', autouse=True)
# def set_db_name():
#     """Set the database name for the test session."""
#     environ['DB_NAME'] = 'an_app_{}'.format(int(time()))


@pytest.fixture(scope='session', autouse=True)
# def run_docker(set_db_name):
def run_docker():
    """Run docker containers for integration tests."""
    this_dir = path.abspath(path.dirname(__file__))
    root_dir = path.abspath(path.join(this_dir, '../..'))
    chdir(root_dir)
    Popen(('docker-compose', 'up', '-d')).communicate()
    sleep(5)
    yield
    Popen(('docker-compose', 'down', '-v')).communicate()
