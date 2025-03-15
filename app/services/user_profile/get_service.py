from fastapi import HTTPException

from app.models.user_profile import UserProfile


def get_service(profile_id, db):
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()

    if profile is None:
        raise HTTPException(status_code=404, detail="Not found")

    return profile
