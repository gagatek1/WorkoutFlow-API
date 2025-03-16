from fastapi import HTTPException

from app.models.user_profile import UserProfile
from app.models.workout import Workout


def get_workout(workout_id, db, user):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.get("Username"))
        .first()
    )
    if workout is None:
        raise HTTPException(status_code=404, detail="Not found")

    if workout.profile_id == profile.id:
        return workout

    raise HTTPException(status_code=401, detail="Not authorized")


def get_workouts(db, user):
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.get("Username"))
        .first()
    )
    workouts = db.query(Workout).filter(Workout.profile_id == profile.id).all()

    return workouts
