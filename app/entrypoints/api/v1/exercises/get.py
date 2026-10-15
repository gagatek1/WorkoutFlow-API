from typing import Annotated

from fastapi import APIRouter, Path, Request

from app.domain.exercise.query_service import ExerciseQueryService
from app.domain.exercise.schemas import ExerciseResponse
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["exercises"])

EXERCISE_QUERY_SERVICE = ExerciseQueryService()


@router.get("/workouts/{workout_id}/exercises/{exercise_id}", description="Get an exercise of the caller's workout.")
def show_exercise(
    workout_id: Annotated[str, Path(pattern=ID_PATTERN, description="Workout id")],
    exercise_id: Annotated[str, Path(pattern=ID_PATTERN, description="Exercise id")],
    request: Request,
) -> ExerciseResponse:
    with authorize_user(request.headers) as user:
        return EXERCISE_QUERY_SERVICE.get_exercise(workout_id, exercise_id, user.id)
