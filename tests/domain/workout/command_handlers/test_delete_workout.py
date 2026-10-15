import pytest

from app.domain.profile.query_service import ProfileQueryService
from app.domain.workout.command_handlers.delete_workout import delete_workout_handler
from app.domain.workout.commands.delete_workout import DeleteWorkoutCommand
from app.domain.workout.exceptions import WorkoutHasExercisesError, WorkoutNotFoundError
from app.domain.workout.query_service import WorkoutQueryService
from tests.fixtures.factories import ExerciseModelFactory, ProfileModelFactory, WorkoutModelFactory


def _delete(workout_id: str, actor: str) -> None:
    delete_workout_handler(DeleteWorkoutCommand(workout_id=workout_id, actor_id=actor))


@pytest.mark.usefixtures("db")
class TestDeleteWorkoutHandler:
    def test_owner_deletes_and_profile_count_drops(self) -> None:
        ProfileModelFactory.create(workout_quantity=1)
        workout = WorkoutModelFactory.create()

        _delete(workout.id, "alice")

        with pytest.raises(WorkoutNotFoundError):
            WorkoutQueryService().get_workout(workout.id, "alice")
        assert ProfileQueryService().get_profile("alice").workout_quantity == 0

    def test_other_user_gets_not_found(self) -> None:
        workout = WorkoutModelFactory.create()

        with pytest.raises(WorkoutNotFoundError):
            _delete(workout.id, "mallory")

        assert WorkoutQueryService().get_workout(workout.id, "alice").id == workout.id

    def test_workout_with_exercises_is_refused(self) -> None:
        exercise = ExerciseModelFactory.create()

        with pytest.raises(WorkoutHasExercisesError):
            _delete(exercise.workout_id, "alice")

        assert WorkoutQueryService().get_workout(exercise.workout_id, "alice").id == exercise.workout_id
