from app.domain.profile.commands.update_profile import UpdateProfileCommand
from app.domain.profile.entity import ProfileModel
from app.domain.profile.repository import ProfileRepository
from app.domain.profile.schemas import ProfileResponse
from app.shared.db import unit_of_work


def update_profile_handler(command: UpdateProfileCommand) -> ProfileResponse:
    with unit_of_work() as session:
        profiles = ProfileRepository(session)
        profile = profiles.find_for_update(command.user_id)
        if profile is None:
            profile = ProfileModel(
                user_id=command.user_id,
                first_name=command.first_name,
                last_name=command.last_name,
                total_weight=0,
                workout_quantity=0,
            )
            profiles.add(profile)
        profile.first_name = command.first_name
        profile.last_name = command.last_name
        return ProfileResponse.model_validate(profile)
