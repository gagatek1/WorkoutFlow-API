from fastapi import HTTPException

from app.models.user import User
from app.models.workout import Workout
from app.schemas.workout import Workout as UpdateWorkout


def update_service(workout_id: int, data: UpdateWorkout, db, cognito_user):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()

    user = (
        db.query(User)
        .filter(User.cognito_id == cognito_user.get("Username"))
        .first()
    )

    if user.id != workout.user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    else:
        if data.name is not None:
            workout.name = data.name
        if data.date is not None:
            workout.date = data.date

    db.commit()
    db.refresh(workout)

    return workout
