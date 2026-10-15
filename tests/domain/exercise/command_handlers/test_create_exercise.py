import pytest

from app.domain.exercise.command_handlers.create_exercise import create_exercise_handler
from app.domain.exercise.commands.create_exercise import CreateExerciseCommand
from app.domain.exercise.query_service import ExerciseQueryService
from app.domain.exercise.schemas import ExercisePart, ExerciseResponse
from app.domain.profile.query_service import ProfileQueryService
from app.domain.workout.exceptions import WorkoutNotFoundError
from app.domain.workout.query_service import WorkoutQueryService
from tests.fixtures.factories import WorkoutModelFactory


def _create(workout_id: str, actor: str = "alice") -> ExerciseResponse:
    return create_exercise_handler(
        CreateExerciseCommand(
            workout_id=workout_id, actor_id=actor, name="Bench", sets=3, reps=10, weight=50, part=ExercisePart.CHEST
        )
    )


@pytest.mark.usefixtures("db")
class TestCreateExerciseHandler:
    def test_persists_and_adds_volume_to_workout_and_profile(self) -> None:
        workout = WorkoutModelFactory.create()

        exercise = _create(workout.id)

        assert ExerciseQueryService().get_exercise(workout.id, exercise.id, "alice") == exercise
        assert WorkoutQueryService().get_workout(workout.id, "alice").total_weight == 1500
        assert ProfileQueryService().get_profile("alice").total_weight == 1500

    def test_someone_elses_workout_is_not_found(self) -> None:
        workout = WorkoutModelFactory.create(owner_id="bob")

        with pytest.raises(WorkoutNotFoundError):
            _create(workout.id)

        assert WorkoutQueryService().get_workout(workout.id, "bob").total_weight == 0
