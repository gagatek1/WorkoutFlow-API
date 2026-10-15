from collections.abc import Generator
from contextlib import contextmanager
from functools import cache
from typing import Any

from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.settings import database_settings

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class OrmBase(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


@cache
def get_engine() -> Engine:
    url = database_settings.url.get_secret_value()
    options: dict[str, Any] = {"echo": database_settings.echo, "hide_parameters": True}
    if url.startswith("sqlite"):
        options |= {"poolclass": StaticPool, "connect_args": {"check_same_thread": False}}
    else:
        options |= {"pool_size": database_settings.pool_size, "max_overflow": 0, "pool_pre_ping": True}
    return create_engine(url, **options)


@cache
def _session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


@contextmanager
def unit_of_work() -> Generator[Session]:
    with _session_factory().begin() as session:
        yield session
