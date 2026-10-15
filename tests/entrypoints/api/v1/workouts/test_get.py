import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import WorkoutModelFactory


@pytest.mark.usefixtures("db")
class TestGetWorkoutEndpoint:
    def test_owner_gets_workout(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()

        response = client.get(f"/api/v1/workouts/{workout.id}", headers=tokens.of("alice"))

        assert response.status_code == 200
        assert response.json()["id"] == workout.id

    def test_other_user_and_missing_are_404_invalid_id_is_422(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()

        assert client.get(f"/api/v1/workouts/{workout.id}", headers=tokens.of("bob")).status_code == 404
        assert client.get("/api/v1/workouts/missing", headers=tokens.of("alice")).status_code == 404
        assert client.get("/api/v1/workouts/a%20b", headers=tokens.of("alice")).status_code == 422
