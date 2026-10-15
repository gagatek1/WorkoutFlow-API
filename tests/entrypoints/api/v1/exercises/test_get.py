import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ExerciseModelFactory, WorkoutModelFactory


@pytest.mark.usefixtures("db")
class TestGetExerciseEndpoint:
    def test_owner_reads_and_outsider_gets_404(self, client: TestClient, tokens: Tokens) -> None:
        exercise = ExerciseModelFactory.create()
        url = f"/api/v1/workouts/{exercise.workout_id}/exercises/{exercise.id}"

        assert client.get(url, headers=tokens.of("alice")).json()["part"] == "chest"
        assert client.get(url, headers=tokens.of("bob")).status_code == 404

    def test_exercise_from_another_workout_is_404(self, client: TestClient, tokens: Tokens) -> None:
        exercise = ExerciseModelFactory.create()
        other = WorkoutModelFactory.create()

        url = f"/api/v1/workouts/{other.id}/exercises/{exercise.id}"
        assert client.get(url, headers=tokens.of("alice")).status_code == 404
