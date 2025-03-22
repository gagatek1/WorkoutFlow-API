from fastapi import APIRouter, Depends

from app.core.database import db_dependency
from app.core.security import get_token
from app.schemas.exercise import Exercise
from app.services.exercise.create_service import create_service

exercise_router = APIRouter(prefix="/exercises", tags=["exercises"])


@exercise_router.post("/create")
async def create_exercise(
    data: Exercise, db: db_dependency, user: dict = Depends(get_token)
):
    return create_service(data, db, user)
