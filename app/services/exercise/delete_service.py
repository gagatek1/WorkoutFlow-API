from fastapi import HTTPException

from app.models.exercise import Exercise
from app.models.user_profile import UserProfile


def delete_service(exercise_id, db, user):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.get("Username"))
        .first()
    )

    if exercise is None:
        raise HTTPException(status_code=404, detail="Not found")
    if exercise.workout.profile_id == profile.id:
        exercise_total_weight = exercise.weight * exercise.sets * exercise.reps
        profile.total_weight -= exercise_total_weight
        exercise.workout.total_weight -= exercise_total_weight

        db.delete(exercise)
        db.commit()
    else:
        raise HTTPException(status_code=401, detail="Not authorized")
