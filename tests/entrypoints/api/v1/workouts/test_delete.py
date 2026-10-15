import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ExerciseModelFactory, ProfileModelFactory, WorkoutModelFactory


@pytest.mark.usefixtures("db")
class TestDeleteWorkoutEndpoint:
    def test_owner_deletes(self, client: TestClient, tokens: Tokens) -> None:
        ProfileModelFactory.create(workout_quantity=1)
        workout = WorkoutModelFactory.create()
        headers = tokens.of("alice")

        assert client.delete(f"/api/v1/workouts/{workout.id}", headers=headers).status_code == 204
        assert client.get(f"/api/v1/workouts/{workout.id}", headers=headers).status_code == 404

    def test_other_user_is_404(self, client: TestClient, tokens: Tokens) -> None:
        workout = WorkoutModelFactory.create()

        assert client.delete(f"/api/v1/workouts/{workout.id}", headers=tokens.of("bob")).status_code == 404

    def test_workout_with_exercises_is_409(self, client: TestClient, tokens: Tokens) -> None:
        exercise = ExerciseModelFactory.create()

        assert client.delete(f"/api/v1/workouts/{exercise.workout_id}", headers=tokens.of("alice")).status_code == 409
