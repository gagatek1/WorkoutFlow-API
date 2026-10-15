import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import WorkoutModelFactory

BODY = {"name": "Legs", "date": "2026-02-02"}


@pytest.mark.usefixtures("db")
class TestUpdateWorkoutEndpoint:
    def test_owner_updates(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()

        response = client.put(f"/api/v1/workouts/{workout.id}", json=BODY, headers=tokens.of("alice"))

        assert response.status_code == 200
        assert (response.json()["name"], response.json()["date"]) == ("Legs", "2026-02-02")

    def test_other_user_is_404(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()

        assert client.put(f"/api/v1/workouts/{workout.id}", json=BODY, headers=tokens.of("bob")).status_code == 404

    def test_date_is_required(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()

        assert (
            client.put(f"/api/v1/workouts/{workout.id}", json={"name": "Legs"}, headers=tokens.of("alice")).status_code
            == 422
        )
