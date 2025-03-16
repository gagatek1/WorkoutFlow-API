from fastapi import APIRouter, Depends
from starlette import status

from app.core.database import db_dependency
from app.core.security import get_token
from app.schemas.workout import Workout
from app.services.workout.create_service import create_service
from app.services.workout.delete_service import delete_service
from app.services.workout.get_service import get_workout, get_workouts
from app.services.workout.update_service import update_service

workout_router = APIRouter(prefix="/workouts", tags=["workouts"])


@workout_router.post("/create")
async def create_workout(
    data: Workout, db: db_dependency, user: dict = Depends(get_token)
):
    return create_service(data, db, user)


@workout_router.put("/update/{workout_id}")
async def update_workout(
    workout_id, data: Workout, db: db_dependency, user: dict = Depends(get_token)
):
    return update_service(workout_id, data, db, user)


@workout_router.get("/{workout_id}")
async def show_workout(workout_id, db: db_dependency, user: dict = Depends(get_token)):
    return get_workout(workout_id, db, user)


@workout_router.get("/")
async def show_workouts(db: db_dependency, user: dict = Depends(get_token)):
    return get_workouts(db, user)


@workout_router.delete("/delete/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
    workout_id, db: db_dependency, user: dict = Depends(get_token)
):
    delete_service(workout_id, db, user)
