import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import WorkoutModelFactory

EXERCISE = {"name": "Bench", "sets": 3, "reps": 10, "weight": 50, "part": "chest"}


@pytest.mark.usefixtures("db")
class TestDeleteExerciseEndpoint:
    def test_owner_deletes_and_totals_drop(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()
        headers = tokens.of("alice")
        created = client.post(f"/api/v1/workouts/{workout.id}/exercises", json=EXERCISE, headers=headers).json()
        url = f"/api/v1/workouts/{workout.id}/exercises/{created['id']}"

        assert client.delete(url, headers=tokens.of("bob")).status_code == 404
        assert client.delete(url, headers=headers).status_code == 204
        assert client.delete(url, headers=headers).status_code == 404
        assert client.get(f"/api/v1/workouts/{workout.id}", headers=headers).json()["total_weight"] == 0
