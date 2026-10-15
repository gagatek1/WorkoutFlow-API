from typing import Annotated

from fastapi import APIRouter, Path, Request

from app.domain.workout.query_service import WorkoutQueryService
from app.domain.workout.schemas import WorkoutResponse
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["workouts"])

WORKOUT_QUERY_SERVICE = WorkoutQueryService()


@router.get("/workouts/{workout_id}", description="Get one of the caller's workouts.")
def show_workout(
    workout_id: Annotated[str, Path(pattern=ID_PATTERN, description="Workout id")], request: Request
) -> WorkoutResponse:
    with authorize_user(request.headers) as user:
        return WORKOUT_QUERY_SERVICE.get_workout(workout_id, user.id)
