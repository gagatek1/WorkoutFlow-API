from collections.abc import Iterator

import pytest

import app.domain.exercise.entity
import app.domain.profile.entity
import app.domain.workout.entity  # noqa: F401
from app.shared.db import OrmBase, get_engine


@pytest.fixture
def db() -> Iterator[None]:
    engine = get_engine()
    if engine.dialect.name == "sqlite":
        with engine.connect() as connection:
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")
    OrmBase.metadata.create_all(engine)
    yield
    OrmBase.metadata.drop_all(engine)
