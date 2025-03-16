from fastapi import HTTPException

from app.models.user_profile import UserProfile
from app.models.workout import Workout


def delete_service(workout_id, db, user):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.get("Username"))
        .first()
    )

    if workout is None:
        raise HTTPException(status_code=404, detail="Not found")
    if workout.profile_id == profile.id:
        db.delete(workout)
        db.commit()
    else:
        raise HTTPException(status_code=401, detail="Not authorized")
