from typing import Annotated

from fastapi import APIRouter, Query, Request

from app.domain.workout.query_service import WorkoutQueryService
from app.domain.workout.schemas import WorkoutListResponse
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["workouts"])

WORKOUT_QUERY_SERVICE = WorkoutQueryService()


@router.get("/workouts", description="List the caller's workouts, paginated with next_cursor.")
def show_workouts(
    request: Request,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    cursor: Annotated[str | None, Query(max_length=2048)] = None,
) -> WorkoutListResponse:
    with authorize_user(request.headers) as user:
        return WORKOUT_QUERY_SERVICE.list_workouts(user.id, limit, cursor)
