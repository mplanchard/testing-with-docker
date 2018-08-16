"""Setup file for pypiserver-passlib."""

from os import path
from setuptools import find_packages, setup


NAME = 'an-app'
MAINTAINER = 'Matthew Planchard'
MAINTAINER_EMAIL = 'msplanchard@gmail.com'
URL = 'https://github.com/mplanchard/testing-with-docker'


DESCRIPTION = 'Demonstration app for docker testing'
ENTRY_POINTS = {}
EXTRAS = {}
# Note: drop virtualenv requirement when we drop Python 2 support.
INSTALL_REQUIRES = []
PACKAGE_DATA = {}
PYTHON_REQUIRES = '>3.4'
README = 'README.md'  # relative (to root dir) path to README
SETUP_REQUIRES = ['setuptools', 'wheel']
THIS_DIR = path.abspath(path.dirname(__file__))
VERSION_FILE = 'an_app/_version.py'  # relative to root dir


# https://pypi.org/pypi?%3Aaction=list_classifiers for a full list
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Framework :: Pytest",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Testing",
]


def relpath(strpath):
    """Return a path relative to the repository root."""
    return path.abspath(path.join(THIS_DIR, strpath))


def get_long_description(readme):
    """Parse readme to get the long description."""
    with open(relpath(readme)) as fp:
        return fp.read()


def get_packages():
    """Retrieve packages."""
    return find_packages(
        exclude=('tests', 'tests.*', '*.tests', '*.tests.*')
    )


def get_version(version_file):
    """Parse the version file to retrieve the version."""
    fake_globals = {}
    with open(relpath(version_file)) as vf:
        for ln in vf:
            if ln.startswith('__version'):
                exec(ln, fake_globals)
    return fake_globals['__version__']


setup(
    classifiers=CLASSIFIERS,
    entry_points=ENTRY_POINTS,
    extras_require=EXTRAS,
    install_requires=INSTALL_REQUIRES,
    name=NAME,
    description=DESCRIPTION,
    long_description=get_long_description(README),
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    packages=get_packages(),
    package_data=PACKAGE_DATA,
    python_requires=PYTHON_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    version=get_version(VERSION_FILE),
    url=URL,
)
