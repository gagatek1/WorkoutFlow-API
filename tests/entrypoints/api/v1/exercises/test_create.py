import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import WorkoutModelFactory

EXERCISE = {"name": "Bench", "sets": 3, "reps": 10, "weight": 50, "part": "chest"}


@pytest.mark.usefixtures("db")
class TestCreateExerciseEndpoint:
    def test_creates_exercise_and_updates_totals(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()
        headers = tokens.of("alice")

        response = client.post(f"/api/v1/workouts/{workout.id}/exercises", json=EXERCISE, headers=headers)

        assert response.status_code == 201
        assert response.json()["workout_id"] == workout.id
        assert client.get(f"/api/v1/workouts/{workout.id}", headers=headers).json()["total_weight"] == 1500
        assert client.get("/api/v1/profiles/me", headers=headers).json()["total_weight"] == 1500

    def test_someone_elses_workout_is_404(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create(owner_id="bob")

        response = client.post(f"/api/v1/workouts/{workout.id}/exercises", json=EXERCISE, headers=tokens.of("alice"))

        assert response.status_code == 404

    @pytest.mark.parametrize(
        "change", [{"sets": 0}, {"reps": -1}, {"weight": -5}, {"part": "neck"}, {"name": ""}, {"workout_id": "x"}]
    )
    def test_rejects_invalid_body(self, client: TestClient, tokens: Tokens, change: dict[str, object]) -> None:
        url = f"/api/v1/workouts/{WorkoutModelFactory.create().id}/exercises"

        assert client.post(url, json={**EXERCISE, **change}, headers=tokens.of("alice")).status_code == 422
