from app.domain.profile.entity import ProfileModel
from app.domain.profile.exceptions import ProfileNotFoundError
from app.domain.profile.schemas import ProfileResponse
from app.shared.db import unit_of_work


class ProfileQueryService:
    def get_profile(self, user_id: str) -> ProfileResponse:
        with unit_of_work() as session:
            profile = session.get(ProfileModel, user_id)
            if profile is None:
                raise ProfileNotFoundError
            return ProfileResponse.model_validate(profile)
