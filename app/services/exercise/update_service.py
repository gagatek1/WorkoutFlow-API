from math import expm1

from fastapi import HTTPException

from app.models.exercise import Exercise
from app.models.user_profile import UserProfile
from app.schemas.exercise import UpdateExercise


def update_service(exercise_id: int, data: UpdateExercise, db, user):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()

    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.get("Username"))
        .first()
    )

    if profile.id != exercise.workout.profile_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    else:
        workout_total_weight = exercise.workout.total_weight
        old_exercise_weight = exercise.weight * exercise.sets * exercise.reps
        if data.name is not None:
            exercise.name = data.name
        if data.sets is not None:
            exercise.sets = data.sets
        if data.reps_in_set is not None:
            exercise.reps = data.reps_in_set
        if data.weight is not None:
            exercise.weight = data.weight
        if data.part is not None:
            exercise.part = data.part

        new_exercise_weight = exercise.weight * exercise.sets * exercise.reps
        exercise.workout.total_weight = (
            workout_total_weight - old_exercise_weight + new_exercise_weight
        )
        profile.total_weight = (
            profile.total_weight - old_exercise_weight + new_exercise_weight
        )

    db.commit()
    db.refresh(exercise)

    return exercise
