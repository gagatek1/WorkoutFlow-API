from app.domain.profile.commands.create_profile import CreateProfileCommand
from app.domain.profile.entity import ProfileModel
from app.domain.profile.repository import ProfileRepository
from app.domain.profile.schemas import ProfileResponse
from app.shared.db import unit_of_work


def create_profile_handler(command: CreateProfileCommand) -> ProfileResponse:
    with unit_of_work() as session:
        profile = ProfileModel(
            user_id=command.user_id,
            first_name=command.first_name,
            last_name=command.last_name,
            total_weight=0,
            workout_quantity=0,
        )
        ProfileRepository(session).add(profile)
        return ProfileResponse.model_validate(profile)
