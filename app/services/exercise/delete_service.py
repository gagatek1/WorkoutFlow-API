from fastapi import HTTPException

from app.models.exercise import Exercise
from app.models.user import User


def delete_service(exercise_id, db, cognito_user):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    user = (
        db.query(User).filter(User.cognito_id == cognito_user.get("Username")).first()
    )

    if exercise is None:
        raise HTTPException(status_code=404, detail="Not found")
    if exercise.workout.user_id == user.id:
        exercise_total_weight = exercise.weight * exercise.sets * exercise.reps
        user.total_weight -= exercise_total_weight
        exercise.workout.total_weight -= exercise_total_weight

        db.delete(exercise)
        db.commit()
    else:
        raise HTTPException(status_code=401, detail="Not authorized")
