from typing import Annotated

from fastapi import APIRouter, Path, Query, Request

from app.domain.exercise.query_service import ExerciseQueryService
from app.domain.exercise.schemas import ExerciseListResponse
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["exercises"])

EXERCISE_QUERY_SERVICE = ExerciseQueryService()


@router.get("/workouts/{workout_id}/exercises", description="List exercises of the caller's workout, paginated.")
def show_exercises(
    workout_id: Annotated[str, Path(pattern=ID_PATTERN, description="Workout id")],
    request: Request,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    cursor: Annotated[str | None, Query(max_length=2048)] = None,
) -> ExerciseListResponse:
    with authorize_user(request.headers) as user:
        return EXERCISE_QUERY_SERVICE.list_exercises(workout_id, user.id, limit, cursor)
