from fastapi import HTTPException

from app.models.exercise import Exercise
from app.models.user import User
from app.models.workout import Workout


def get_exercise(exercise_id, db, cognito_user):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    user = (
        db.query(User)
        .filter(User.cognito_id == cognito_user.get("Username"))
        .first()
    )
    if exercise is None:
        raise HTTPException(status_code=404, detail="Not found")

    if exercise.workout.profile_id == user.id:
        return exercise

    raise HTTPException(status_code=401, detail="Not authorized")


def get_exercises(db, cognito_user):
    user = (
        db.query(User)
        .filter(User.cognito_id == cognito_user.get("Username"))
        .first()
    )
    exercises = (
        db.query(Exercise)
        .join(Exercise.workout)
        .filter(Workout.user_id == user.id)
        .all()
    )

    return exercises
