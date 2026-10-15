import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import WorkoutModelFactory


@pytest.mark.usefixtures("db")
class TestListWorkoutsEndpoint:
    def test_lists_only_callers_workouts_paginated(self, client: TestClient, tokens: Tokens) -> None:
        mine = {w.id for w in WorkoutModelFactory.create_batch(3)}
        WorkoutModelFactory.create(owner_id="bob")
        headers = tokens.of("alice")

        first = client.get("/api/v1/workouts?limit=2", headers=headers).json()
        second = client.get(f"/api/v1/workouts?limit=2&cursor={first['next_cursor']}", headers=headers).json()

        assert len(first["items"]) == 2
        assert {w["id"] for w in first["items"] + second["items"]} == mine

    @pytest.mark.parametrize("limit", [0, 101])
    def test_rejects_invalid_limit(self, client: TestClient, tokens: Tokens, limit: int) -> None:
        assert client.get(f"/api/v1/workouts?limit={limit}", headers=tokens.of("alice")).status_code == 422
