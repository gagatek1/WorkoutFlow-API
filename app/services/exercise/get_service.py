from fastapi import HTTPException
from sqlalchemy.orm import load_only

from app.models.exercise import Exercise
from app.models.user_profile import UserProfile
from app.models.workout import Workout


def get_exercise(exercise_id, db, user):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.get("Username"))
        .first()
    )
    if exercise is None:
        raise HTTPException(status_code=404, detail="Not found")

    if exercise.workout.profile_id == profile.id:
        return exercise

    raise HTTPException(status_code=401, detail="Not authorized")


def get_exercises(db, user):
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.get("Username"))
        .first()
    )
    exercises = (
        db.query(Exercise)
        .join(Exercise.workout)
        .filter(Workout.profile_id == profile.id)
        .all()
    )

    return exercises
