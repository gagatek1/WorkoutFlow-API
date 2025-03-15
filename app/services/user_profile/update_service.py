from fastapi import HTTPException

from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfile as UpdateProfile


def update_service(profile_id, update_profile: UpdateProfile, db, user):
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()

    user_id = user.get("Username")

    if user_id != profile.user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    else:
        if update_profile.first_name is not None:
            profile.first_name = update_profile.first_name
        if update_profile.last_name is not None:
            profile.last_name = update_profile.last_name

        db.commit()
        db.refresh(profile)

        return profile
