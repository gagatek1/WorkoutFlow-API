import pytest

from app.domain.profile.command_handlers.create_profile import create_profile_handler
from app.domain.profile.commands.create_profile import CreateProfileCommand
from app.domain.profile.exceptions import ProfileAlreadyExistsError
from app.domain.profile.query_service import ProfileQueryService

COMMAND = CreateProfileCommand(user_id="alice", first_name=" Alice ", last_name="Smith")


@pytest.mark.usefixtures("db")
class TestCreateProfileHandler:
    def test_persists_with_zero_totals(self) -> None:
        profile = create_profile_handler(COMMAND)

        assert (profile.id, profile.first_name, profile.total_weight, profile.workout_quantity) == (
            "alice",
            "Alice",
            0,
            0,
        )
        assert ProfileQueryService().get_profile("alice") == profile

    def test_duplicate_is_rejected(self) -> None:
        create_profile_handler(COMMAND)

        with pytest.raises(ProfileAlreadyExistsError):
            create_profile_handler(COMMAND)
