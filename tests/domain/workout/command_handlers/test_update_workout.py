from datetime import date

import pytest

from app.domain.workout.command_handlers.update_workout import update_workout_handler
from app.domain.workout.commands.update_workout import UpdateWorkoutCommand
from app.domain.workout.exceptions import WorkoutNotFoundError
from app.domain.workout.query_service import WorkoutQueryService
from app.domain.workout.schemas import WorkoutResponse
from tests.fixtures.factories import WorkoutModelFactory


def _update(workout_id: str, actor: str) -> WorkoutResponse:
    return update_workout_handler(
        UpdateWorkoutCommand(workout_id=workout_id, actor_id=actor, name="Legs", date=date(2026, 2, 2))
    )


@pytest.mark.usefixtures("db")
class TestUpdateWorkoutHandler:
    def test_owner_changes_fields_and_keeps_total(self) -> None:
        workout = WorkoutModelFactory.create(total_weight=300)

        updated = _update(workout.id, "alice")

        assert (updated.name, updated.date, updated.total_weight) == ("Legs", date(2026, 2, 2), 300)
        assert WorkoutQueryService().get_workout(workout.id, "alice") == updated

    def test_other_user_gets_not_found_and_item_is_unchanged(self) -> None:
        workout = WorkoutModelFactory.create()

        with pytest.raises(WorkoutNotFoundError):
            _update(workout.id, "mallory")

        assert WorkoutQueryService().get_workout(workout.id, "alice").name == workout.name

    def test_missing_workout_raises_not_found(self) -> None:
        with pytest.raises(WorkoutNotFoundError):
            _update("missing", "alice")
