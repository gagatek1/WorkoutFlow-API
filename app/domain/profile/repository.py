from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.profile.entity import ProfileModel
from app.domain.profile.exceptions import ProfileAlreadyExistsError, ProfileNotFoundError


class ProfileRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, profile: ProfileModel) -> None:
        self._session.add(profile)
        try:
            self._session.flush()
        except IntegrityError as exc:
            raise ProfileAlreadyExistsError from exc

    def find_for_update(self, user_id: str) -> ProfileModel | None:
        return self._session.scalar(select(ProfileModel).where(ProfileModel.user_id == user_id).with_for_update())

    def get_for_update(self, user_id: str) -> ProfileModel:
        profile = self.find_for_update(user_id)
        if profile is None:
            raise ProfileNotFoundError
        return profile
