from fastapi import HTTPException

from app.models.exercise import Exercise as ExerciseModel
from app.models.user_profile import UserProfile
from app.models.workout import Workout as Workout
from app.schemas.exercise import Exercise


def create_service(data: Exercise, db, user):
    workout = db.query(Workout).filter(Workout.id == data.workout_id).first()
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.get("Username"))
        .first()
    )

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    if workout.profile_id != profile.id:
        raise HTTPException(status_code=401, detail="Not authorized")

    new_exercise = ExerciseModel(
        name=data.name,
        sets=data.sets,
        reps=data.reps_in_set,
        part=data.part,
        weight=data.weight,
        workout_id=workout.id,
    )

    total_weight = workout.total_weight + data.weight * data.sets * data.reps_in_set
    workout.total_weight = total_weight

    profile.total_weight += data.weight * data.sets * data.reps_in_set

    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)

    return new_exercise
