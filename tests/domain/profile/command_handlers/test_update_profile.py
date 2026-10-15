import pytest

from app.domain.profile.command_handlers.update_profile import update_profile_handler
from app.domain.profile.commands.update_profile import UpdateProfileCommand
from app.domain.profile.query_service import ProfileQueryService
from tests.fixtures.factories import ProfileModelFactory


@pytest.mark.usefixtures("db")
class TestUpdateProfileHandler:
    def test_changes_names_and_keeps_totals(self) -> None:
        ProfileModelFactory.create(total_weight=500, workout_quantity=2)

        updated = update_profile_handler(UpdateProfileCommand(user_id="alice", first_name="Ala", last_name="Nowak"))

        assert (updated.first_name, updated.last_name, updated.total_weight, updated.workout_quantity) == (
            "Ala",
            "Nowak",
            500,
            2,
        )
        assert ProfileQueryService().get_profile("alice") == updated

    def test_creates_missing_profile_with_zero_totals(self) -> None:
        created = update_profile_handler(UpdateProfileCommand(user_id="ghost", first_name="A", last_name="B"))

        assert (created.id, created.total_weight, created.workout_quantity) == ("ghost", 0, 0)
        assert ProfileQueryService().get_profile("ghost") == created
