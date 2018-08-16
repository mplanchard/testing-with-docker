"""Database operations and configuration."""

from functools import partial
from typing import Iterable, Mapping, Tuple

import asyncpg
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    Sequence,
    String,
    Table,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import Engine
from sqlalchemy.schema import CreateTable


def sql_compile(dialect, statement, incl_literal_binds=True):
    """Compile a statement for the given dialect."""
    return statement.compile(
        dialect=dialect,
        compile_kwargs={'literal_binds': True} if incl_literal_binds else {}
    )


pg_compile = partial(sql_compile, postgresql.dialect())


def db_url(env: Mapping[str, str]) -> str:
    """Return a DB url for postgres."""
    return (
        'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}'
        '/{DB_NAME}'.format(**env)
    )


async def get_connection(env: Mapping[str, str]) -> Engine:
    """Return a new engine instance."""
    return await asyncpg.connect(db_url(env))


def get_metadata() -> MetaData:
    """Return a metadata instance with added tables."""
    metadata = MetaData()
    Table(
        'user',
        metadata,
        Column(
            'id',
            Integer,
            Sequence('user_id_seq', metadata=metadata),
            primary_key=True
        ),
        Column('email', String(256), unique=True),
        Column('password', String(512)),
    )
    return metadata


def get_tables(metadata: MetaData) -> Iterable[Tuple[str, Table]]:
    """Retrieve table references from the metadata."""
    return map(
        lambda t: (t.name, t),
        metadata.sorted_tables,
    )


async def create_tables(con: asyncpg.Connection, metadata: MetaData) -> None:
    """Create tables for a metadata instance."""
    extant_tables = list(map(
        lambda r: r['table_name'],
        await con.fetch(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema='public'"
        )
    ))
    async with con.transaction():
        for table in metadata.sorted_tables:
            if table.name not in extant_tables:
                await con.execute(str(CreateTable(table)))
