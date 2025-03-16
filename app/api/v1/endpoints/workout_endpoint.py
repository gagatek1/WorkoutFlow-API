from fastapi import APIRouter, Depends

from app.core.database import db_dependency
from app.core.security import get_token
from app.schemas.workout import Workout
from app.services.workout.create_service import create_service
from app.services.workout.update_service import update_service

workout_router = APIRouter(prefix="/workout", tags=["workout"])


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
