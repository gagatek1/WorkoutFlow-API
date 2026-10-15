import pytest

from app.domain.exercise.command_handlers.create_exercise import create_exercise_handler
from app.domain.exercise.command_handlers.update_exercise import update_exercise_handler
from app.domain.exercise.commands.create_exercise import CreateExerciseCommand
from app.domain.exercise.commands.update_exercise import UpdateExerciseCommand
from app.domain.exercise.exceptions import ExerciseNotFoundError
from app.domain.exercise.schemas import ExercisePart, ExerciseResponse
from app.domain.profile.query_service import ProfileQueryService
from app.domain.workout.query_service import WorkoutQueryService
from tests.fixtures.factories import WorkoutModelFactory


def _update(workout_id: str, exercise_id: str, actor: str = "alice") -> ExerciseResponse:
    return update_exercise_handler(
        UpdateExerciseCommand(
            workout_id=workout_id,
            exercise_id=exercise_id,
            actor_id=actor,
            name="Squat",
            sets=5,
            reps=5,
            weight=100,
            part=ExercisePart.LEGS,
        )
    )


@pytest.mark.usefixtures("db")
class TestUpdateExerciseHandler:
    def test_replaces_volume_in_totals(self) -> None:
        workout = WorkoutModelFactory.create()
        exercise = create_exercise_handler(
            CreateExerciseCommand(
                workout_id=workout.id, actor_id="alice", name="Bench", sets=3, reps=10, weight=50, part="chest"
            )
        )

        updated = _update(workout.id, exercise.id)

        assert (updated.name, updated.part) == ("Squat", ExercisePart.LEGS)
        assert WorkoutQueryService().get_workout(workout.id, "alice").total_weight == 2500
        assert ProfileQueryService().get_profile("alice").total_weight == 2500

    def test_other_user_and_missing_are_not_found(self) -> None:
        workout = WorkoutModelFactory.create()

        with pytest.raises(ExerciseNotFoundError):
            _update(workout.id, "missing")
