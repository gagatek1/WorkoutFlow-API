from datetime import UTC, date, datetime

import pytest

from app.domain.profile.exceptions import ProfileNotFoundError
from app.domain.profile.query_service import ProfileQueryService
from app.domain.workout.command_handlers.create_workout import create_workout_handler
from app.domain.workout.commands.create_workout import CreateWorkoutCommand
from app.domain.workout.query_service import WorkoutQueryService
from tests.fixtures.factories import ProfileModelFactory


@pytest.mark.usefixtures("db")
class TestCreateWorkoutHandler:
    def test_persists_and_counts_workout_in_profile(self) -> None:
        ProfileModelFactory.create()

        workout = create_workout_handler(CreateWorkoutCommand(owner_id="alice", name="Push", date=date(2026, 5, 1)))

        assert (workout.name, workout.date, workout.total_weight) == ("Push", date(2026, 5, 1), 0)
        assert WorkoutQueryService().get_workout(workout.id, "alice") == workout
        assert ProfileQueryService().get_profile("alice").workout_quantity == 1

    def test_date_defaults_to_today(self) -> None:
        ProfileModelFactory.create()

        assert (
            create_workout_handler(CreateWorkoutCommand(owner_id="alice", name="Pull")).date == datetime.now(UTC).date()
        )

    def test_missing_profile_is_rejected(self) -> None:
        with pytest.raises(ProfileNotFoundError):
            create_workout_handler(CreateWorkoutCommand(owner_id="ghost", name="Legs"))
