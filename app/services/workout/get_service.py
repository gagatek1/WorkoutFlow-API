from fastapi import HTTPException

from app.models.user import User
from app.models.workout import Workout


def get_workout(workout_id, db, cognito_user):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    user = (
        db.query(User).filter(User.cognito_id == cognito_user.get("Username")).first()
    )
    if workout is None:
        raise HTTPException(status_code=404, detail="Not found")

    if workout.user_id == user.id:
        return workout

    raise HTTPException(status_code=401, detail="Not authorized")


def get_workouts(db, cognito_user):
    user = (
        db.query(User).filter(User.cognito_id == cognito_user.get("Username")).first()
    )
    workouts = db.query(Workout).filter(Workout.user_id == user.id).all()

    return workouts
