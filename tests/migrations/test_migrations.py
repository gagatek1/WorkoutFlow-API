from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import inspect

from app.shared.db import OrmBase, get_engine

ALEMBIC_INI = Path(__file__).resolve().parents[2] / "alembic.ini"


def _table_names() -> set[str]:
    return set(inspect(get_engine()).get_table_names()) - {"alembic_version"}


@pytest.fixture(autouse=True)
def _clean_database() -> Iterator[None]:
    yield
    command.downgrade(Config(ALEMBIC_INI), "base")


class TestMigrations:
    def test_upgrade_matches_models_and_downgrade_cleans_up(self) -> None:
        config = Config(ALEMBIC_INI)

        command.upgrade(config, "head")
        with get_engine().connect() as connection:
            diff = compare_metadata(MigrationContext.configure(connection), OrmBase.metadata)
        command.downgrade(config, "base")

        assert diff == []
        assert _table_names() == set()
