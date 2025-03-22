from fastapi import HTTPException

from app.models.user_profile import UserProfile
from app.models.workout import Workout
from app.schemas.workout import Workout as CreateWorkout


def create_service(data: CreateWorkout, db, user):
    if data.name is None:
        raise HTTPException(status_code=422, detail="Name is none")

    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.get("Username"))
        .first()
    )
    new_workout = Workout(name=data.name, date=data.date, profile_id=profile.id)

    profile.workout_quantity += 1

    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return new_workout
