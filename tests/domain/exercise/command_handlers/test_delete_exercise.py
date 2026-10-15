import pytest

from app.domain.exercise.command_handlers.create_exercise import create_exercise_handler
from app.domain.exercise.command_handlers.delete_exercise import delete_exercise_handler
from app.domain.exercise.commands.create_exercise import CreateExerciseCommand
from app.domain.exercise.commands.delete_exercise import DeleteExerciseCommand
from app.domain.exercise.exceptions import ExerciseNotFoundError
from app.domain.profile.query_service import ProfileQueryService
from app.domain.workout.exceptions import WorkoutNotFoundError
from app.domain.workout.query_service import WorkoutQueryService
from tests.fixtures.factories import WorkoutModelFactory


def _delete(workout_id: str, exercise_id: str, actor: str = "alice") -> None:
    delete_exercise_handler(DeleteExerciseCommand(workout_id=workout_id, exercise_id=exercise_id, actor_id=actor))


@pytest.mark.usefixtures("db")
class TestDeleteExerciseHandler:
    def test_removes_volume_from_totals(self) -> None:
        workout = WorkoutModelFactory.create()
        command = CreateExerciseCommand(
            workout_id=workout.id, actor_id="alice", name="Row", sets=3, reps=10, weight=40, part="back"
        )
        kept = create_exercise_handler(command)
        removed = create_exercise_handler(command)

        _delete(workout.id, removed.id)

        with pytest.raises(ExerciseNotFoundError):
            _delete(workout.id, removed.id)
        assert WorkoutQueryService().get_workout(workout.id, "alice").total_weight == 1200
        assert ProfileQueryService().get_profile("alice").total_weight == 1200
        assert kept.id != removed.id

    def test_outsider_is_not_found(self) -> None:
        workout = WorkoutModelFactory.create()
        exercise = create_exercise_handler(
            CreateExerciseCommand(
                workout_id=workout.id, actor_id="alice", name="Row", sets=1, reps=1, weight=1, part="back"
            )
        )

        with pytest.raises(WorkoutNotFoundError):
            _delete(workout.id, exercise.id, actor="bob")
