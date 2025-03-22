from fastapi import APIRouter, Depends

from app.core.database import db_dependency
from app.core.security import get_token
from app.schemas.exercise import Exercise
from app.services.exercise.create_service import create_service
from app.services.exercise.get_service import get_exercise, get_exercises

exercise_router = APIRouter(prefix="/exercises", tags=["exercises"])


@exercise_router.post("/create")
async def create_exercise(
    data: Exercise, db: db_dependency, user: dict = Depends(get_token)
):
    return create_service(data, db, user)


@exercise_router.get("/{exercise_id}")
async def show_exercise(
    exercise_id, db: db_dependency, user: dict = Depends(get_token)
):
    return get_exercise(exercise_id, db, user)


@exercise_router.get("/")
async def show_exercises(db: db_dependency, user: dict = Depends(get_token)):
    return get_exercises(db, user)
