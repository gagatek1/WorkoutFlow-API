from fastapi import HTTPException

from app.models.user_profile import UserProfile
from app.models.workout import Workout
from app.schemas.workout import Workout as UpdateWorkout


def update_service(workout_id: int, data: UpdateWorkout, db, user):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()

    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.get("Username"))
        .first()
    )

    if profile.id != workout.profile_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    else:
        if data.name is not None:
            workout.name = data.name
        if data.date is not None:
            workout.date = data.date

    db.commit()
    db.refresh(workout)

    return workout
