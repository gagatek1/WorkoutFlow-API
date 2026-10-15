import pytest

from app.domain.exercise.exceptions import ExerciseNotFoundError
from app.domain.exercise.query_service import ExerciseQueryService
from app.domain.workout.exceptions import WorkoutNotFoundError
from tests.fixtures.factories import ExerciseModelFactory, WorkoutModelFactory


@pytest.mark.usefixtures("db")
class TestExerciseQueryService:
    def test_list_is_paginated(self) -> None:
        workout = WorkoutModelFactory.create()
        created = {e.id for e in ExerciseModelFactory.create_batch(3, workout_id=workout.id)}

        first = ExerciseQueryService().list_exercises(workout.id, "alice", limit=2)
        second = ExerciseQueryService().list_exercises(workout.id, "alice", limit=2, cursor=first.next_cursor)

        assert len(first.items) == 2
        assert {e.id for e in first.items + second.items} == created

    def test_list_of_someone_elses_workout_is_not_found(self) -> None:
        workout = WorkoutModelFactory.create()

        with pytest.raises(WorkoutNotFoundError):
            ExerciseQueryService().list_exercises(workout.id, "bob", limit=2)

    def test_get_by_outsider_is_not_found(self) -> None:
        exercise = ExerciseModelFactory.create()

        with pytest.raises(ExerciseNotFoundError):
            ExerciseQueryService().get_exercise(exercise.workout_id, exercise.id, "bob")
