from typing import Annotated

from fastapi import APIRouter, Path, Request

from app.domain.workout.command_handlers.update_workout import update_workout_handler
from app.domain.workout.commands.update_workout import UpdateWorkoutCommand
from app.domain.workout.schemas import UpdateWorkoutRequest, WorkoutResponse
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["workouts"])


@router.put("/workouts/{workout_id}", description="Update one of the caller's workouts.")
def update_workout(
    workout_id: Annotated[str, Path(pattern=ID_PATTERN, description="Workout id")],
    body: UpdateWorkoutRequest,
    request: Request,
) -> WorkoutResponse:
    with authorize_user(request.headers) as user:
        return update_workout_handler(
            UpdateWorkoutCommand(workout_id=workout_id, actor_id=user.id, **body.model_dump())
        )
