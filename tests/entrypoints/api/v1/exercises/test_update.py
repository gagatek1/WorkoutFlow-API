import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import WorkoutModelFactory

EXERCISE = {"name": "Bench", "sets": 3, "reps": 10, "weight": 50, "part": "chest"}


@pytest.mark.usefixtures("db")
class TestUpdateExerciseEndpoint:
    def test_owner_updates_and_totals_follow(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()
        headers = tokens.of("alice")
        created = client.post(f"/api/v1/workouts/{workout.id}/exercises", json=EXERCISE, headers=headers).json()
        url = f"/api/v1/workouts/{workout.id}/exercises/{created['id']}"

        response = client.put(url, json={**EXERCISE, "weight": 60}, headers=headers)

        assert response.json()["weight"] == 60
        assert client.get(f"/api/v1/workouts/{workout.id}", headers=headers).json()["total_weight"] == 1800

    def test_outsider_is_404(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()
        created = client.post(
            f"/api/v1/workouts/{workout.id}/exercises", json=EXERCISE, headers=tokens.of("alice")
        ).json()

        url = f"/api/v1/workouts/{workout.id}/exercises/{created['id']}"
        assert client.put(url, json=EXERCISE, headers=tokens.of("bob")).status_code == 404
