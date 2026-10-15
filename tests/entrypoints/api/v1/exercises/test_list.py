import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ExerciseModelFactory, WorkoutModelFactory


@pytest.mark.usefixtures("db")
class TestListExercisesEndpoint:
    def test_lists_workout_exercises(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()
        created = {e.id for e in ExerciseModelFactory.create_batch(2, workout_id=workout.id)}

        response = client.get(f"/api/v1/workouts/{workout.id}/exercises", headers=tokens.of("alice")).json()

        assert {e["id"] for e in response["items"]} == created
        assert response["next_cursor"] is None

    def test_someone_elses_workout_is_404(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()

        assert client.get(f"/api/v1/workouts/{workout.id}/exercises", headers=tokens.of("bob")).status_code == 404
